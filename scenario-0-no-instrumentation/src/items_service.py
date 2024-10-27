from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis import Redis
import json
import os

import websockets
import requests

class RequestCounterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dispatch = None):
        super().__init__(app, dispatch)
        self._request_count = 0

    async def dispatch(self, request, call_next):
        self._request_count += 1
        print(f"Request count: {self._request_count}")
        response = await call_next(request)
        return response


app = FastAPI()
app.add_middleware(RequestCounterMiddleware)

WS_URI = os.getenv("WS_URI", None) # "ws://localhost:8000/ws"
DATA_URI = os.getenv("DATA_URI", None) # "http://localhost:8000/user"
REDIS_URI = os.getenv("REDIS_URI", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = Redis(host=REDIS_URI, port=REDIS_PORT)

@app.get("/ws")
async def say_hi_web_socket():
    async with websockets.connect(uri=WS_URI) as websocket:
        await websocket.send("Hi message from ws client")
        print("Sent ws message")


@app.get("/data")
async def get_data(query:str=None):
    print(query)
    try:
        if query == "fail":
            raise Exception("A really bad error.")
        api_request = requests.get(DATA_URI)
        return JSONResponse(api_request.json())
    except Exception:
        raise HTTPException(status_code=500)


@app.get("/pub")
async def publish_redis_message():
    print("publishing to redis")
    payload = {"message": 'this is my message'}
    redis_client.publish('my-channel', json.dumps(payload))