"""Uptrace span exporter for OpenTelemetry"""

import logging
import typing
from types import MappingProxyType

import lz4.frame
import msgpack
import requests
from opentelemetry import trace as trace_api
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace import export as sdk
from opentelemetry.sdk.util import BoundedDict
from opentelemetry.trace.status import StatusCode

logger = logging.getLogger(__name__)


class Exporter(sdk.SpanExporter):  # pylint:disable=too-many-instance-attributes
    """Uptrace span exporter for OpenTelemetry."""

    def __init__(self, cfg: "Config"):
        self._cfg = cfg
        self._closed = False

        if self._cfg.disabled:
            self._closed = True
            return

    def export(self, spans: typing.Sequence[sdk.Span]) -> sdk.SpanExportResult:
        if self._closed:
            return sdk.SpanExportResult.SUCCESS

        trace_dict = {}

        for span in spans:
            expose = _expo_span(span)

            trace = trace_dict.get(span.context.trace_id)
            if trace is None:
                trace = {"id": _trace_id_bytes(span.context.trace_id), "spans": []}
                trace_dict[span.context.trace_id] = trace

            trace["spans"].append(expose)

        self._send(list(trace_dict.values()))

        return sdk.SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        if self._closed:
            return
        self._closed = True

    def _send(self, traces):
        payload = msgpack.packb({"traces": traces})
        payload = lz4.frame.compress(payload)

        resp = requests.post(
            self._cfg.endpoint, data=payload, headers=self._cfg.headers
        )
        if resp.status_code < 200 or resp.status_code >= 300:
            logger.error("uptrace: status=%d %s", resp.status_code, resp.text)


def _expo_span(span: sdk.Span):
    expose = {
        "id": span.context.span_id,
        "name": span.name,
        "kind": span.kind.value,
        "startTime": span.start_time,
        "endTime": span.end_time,
    }

    if span.parent is not None:
        expose["parentId"] = span.parent.span_id

    if span.status is not None:
        expose["statusCode"] = _expo_status(span.status.status_code)
        if span.status.description:
            expose["statusMessage"] = span.status.description

    if span.attributes:
        expose["attrs"] = _attrs(span.attributes)

    if span.events:
        expose["events"] = _expo_events(span.events)

    if span.links:
        expose["links"] = _expo_links(span.links)

    if span.resource:
        expose["resource"] = _attrs(span.resource.attributes)

    return expose


def _expo_events(events: typing.Sequence[trace_sdk.Event]):
    expose = []
    for evt in events:
        expose.append(
            {"name": evt.name, "attrs": _attrs(evt.attributes), "time": evt.timestamp}
        )
    return expose


def _expo_links(links: typing.Sequence[trace_api.Link]):
    expose = []
    for link in links:
        expose.append(
            {
                "traceId": _trace_id_bytes(link.context.trace_id),
                "spanId": link.context.span_id,
                "attrs": _attrs(link.attributes),
            }
        )
    return expose


def _expo_status(status: StatusCode) -> str:
    if status == StatusCode.ERROR:
        return "error"
    if status == StatusCode.OK:
        return "ok"
    return "unset"


def _attrs(attrs):
    if isinstance(attrs, BoundedDict):
        return attrs._dict  # pylint: disable=protected-access
    if isinstance(attrs, MappingProxyType):
        return attrs.copy()
    return attrs


def _trace_id_bytes(trace_id: int):
    return trace_id.to_bytes(16, byteorder="big")
