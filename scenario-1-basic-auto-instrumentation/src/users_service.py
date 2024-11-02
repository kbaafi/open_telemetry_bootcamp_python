from __future__ import annotations
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import requests
import random
from faker import Faker
import uvicorn
import os
from tracer import init_tracer

REMOTE_USERS_API_URL = os.getenv("REMOTE_USERS_SVC_URI", None)
METRICS_PORT = int(os.getenv("METRICS_PORT", 9000))
TRACES_ENDPOINT = os.getenv("TRACES_ENDPOINT")


meter, tracer = init_tracer(
    service_name="users_service",
    metrics_port=METRICS_PORT,
    traces_endpoint=TRACES_ENDPOINT
)

counter = meter.create_counter("http_requests_total")

class RequestCounterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app, dispatch)
        self._request_count = 0

    async def dispatch(self, request, call_next):
        self._request_count += 1
        counter.add(1, {
            "service": "users_service"
        })
        print(f"Request count: {self._request_count}")
        response = await call_next(request)
        return response


app = FastAPI()
app.add_middleware(RequestCounterMiddleware)
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()


@app.get("/user")
async def get_user():
    with tracer.start_span("user_api_get_user") as active_span:
        api_response = requests.get(REMOTE_USERS_API_URL)
        data = api_response.json()
        random_index = random.randint(0, len(data))
        active_span.add_event(
            name="A number was randomized",
            attributes={"randomIndex": random_index}
        )
    return JSONResponse(content=data[random_index])


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