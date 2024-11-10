from typing import Collection
import websockets
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer, SpanKind
from opentelemetry.propagate import extract, inject
from opentelemetry.trace import SpanKind, Status, StatusCode
import websockets.protocol
from typing import Callable
import json

tracer = get_tracer(
    instrumenting_module_name="CustomWebSocketsInstrumentor",
    instrumenting_library_version="0.0.1"
)


def observe_send(send_func: Callable):
    async def wrapper(self, message):
        with tracer.start_as_current_span("websockets.send", kind=SpanKind.INTERNAL) as span:
            try:
                message_payload = {'message': message}
                inject(message_payload)
                message_str = json.dumps(message_payload)
                await send_func(self, message=message_str)
                print(f"Sending message {message}")
            except Exception as e:
                span.set_status(Status(status_code=StatusCode.ERROR, description=str(e)))
    return wrapper

def observe_recv(recv_func: Callable):
    async def wrapper(self):
        with tracer.start_as_current_span("websockets.recv_wrapper", kind=SpanKind.INTERNAL) as span:
            try:
                message = await(recv_func(self))
                payload = json.loads(message)
                propagation_context = extract(payload)
                message_content = payload['message']
                with tracer.start_as_current_span("websockets.recv", kind=SpanKind.INTERNAL, context=propagation_context) as recv_span:
                    print(f"Received {message_content}")
                    recv_span.add_event("message received")
            except Exception as e:
                span.set_status(Status(status_code=StatusCode.ERROR, description=str(e)))
    return wrapper



class WebSocketsInstrumentor(BaseInstrumentor):
    def __init__(self):
        self._original_send = websockets.WebSocketCommonProtocol.send
        self._original_recv = websockets.WebSocketCommonProtocol.recv


    def _instrument(self, **kwargs):
        websockets.WebSocketCommonProtocol.send = observe_send(websockets.WebSocketCommonProtocol.send)
        websockets.WebSocketCommonProtocol.recv = observe_recv(websockets.WebSocketCommonProtocol.recv)


    def _uninstrument(self, **kwargs):
        # Restore original methods
        websockets.WebSocketCommonProtocol.send = self._original_send
        websockets.WebSocketCommonProtocol.recv = self._original_recv

    def instrumentation_dependencies(self) -> Collection[str]:
        return ['websockets ~= 13.1']
