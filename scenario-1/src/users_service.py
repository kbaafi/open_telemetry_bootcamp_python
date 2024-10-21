from __future__ import annotations
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
import requests
import random
from faker import Faker
from opentelemetry import trace
import uvicorn
import os

app = FastAPI()
fake = Faker()
MAX_LEN = 100

REMOTE_USERS_API_URL = os.getenv("REMOTE_USERS_SVC_URI", None)
tracer = trace.get_tracer(__name__)


@app.get("/user")
async def get_user():
    api_response = requests.get(REMOTE_USERS_API_URL)
    data = api_response.json()
    random_index = random.randint(0, len(data))
    with tracer.start_as_current_span("user_api_get_user") as active_span:
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