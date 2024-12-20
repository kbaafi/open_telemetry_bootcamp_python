from __future__ import annotations

import os
import random

import requests
import uvicorn
from faker import Faker
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette.middleware.base import BaseHTTPMiddleware
from websockets_instrumentor import WebSocketsInstrumentor

from tracer import init_tracer

REMOTE_USERS_API_URL = os.getenv("REMOTE_USERS_SVC_URI", None)
SIGNALS_ENDPOINT = os.getenv("SIGNALS_ENDPOINT")


meter, tracer = init_tracer(
    service_name="users_service",
    signals_endpoint=SIGNALS_ENDPOINT
)

counter = meter.create_counter("http_requests_total")


class RequestCounterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch=None):
        super().__init__(app, dispatch)
        self._request_count = 0

    async def dispatch(self, request, call_next):
        self._request_count += 1
        counter.add(1, {"service": "users_service"})
        print(f"Request count: {self._request_count}")
        response = await call_next(request)
        return response


app = FastAPI()
app.add_middleware(RequestCounterMiddleware)
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
WebSocketsInstrumentor().instrument()


@app.get("/user")
async def get_user():
    with tracer.start_span("user_api_get_user") as active_span:
        api_response = requests.get(REMOTE_USERS_API_URL)
        data = api_response.json()
        random_index = random.randint(0, len(data))
        active_span.add_event(
            name="A number was randomized", attributes={"randomIndex": random_index}
        )
        print(f"TraceId: {active_span.get_span_context().trace_id}")
    return JSONResponse(content=data[random_index-1])


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")
    except WebSocketDisconnect as e:
        print(f"Client disconnected with code: {e.code}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
