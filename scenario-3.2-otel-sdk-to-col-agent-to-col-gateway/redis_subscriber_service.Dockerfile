FROM python:3.10.12-alpine AS build

WORKDIR /home/app

# Create venv
RUN python -m venv venv

# Copy and install requirements
COPY ../requirements.txt requirements.txt
RUN venv/bin/pip install --no-cache-dir --upgrade pip

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy boot.sh and enable excecution
COPY boot_redis_subscriber.sh boot.sh
RUN chmod +x boot.sh

# Copy sources
COPY src/redis_subscriber_service.py app.py
COPY src/tracer.py tracer.py

ENTRYPOINT ["./boot.sh"]