#!/bin/sh
. venv/bin/activate
exec uvicorn app:app --log-level=info --host 0.0.0.0 --port $HTTP_LISTEN_PORT