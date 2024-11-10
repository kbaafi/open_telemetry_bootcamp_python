FROM python:3.10.12-alpine AS build

WORKDIR /home/app

# Set build argument
ARG HTTP_LISTEN_PORT

# Set an environment variable from the argument
ENV HTTP_LISTEN_PORT=${HTTP_LISTEN_PORT}

# Create venv
RUN python -m venv venv

# Copy and install requirements
COPY ../requirements.txt requirements.txt
RUN venv/bin/pip install --no-cache-dir --upgrade pip

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy boot.sh and enable excecution
COPY boot.sh boot.sh
RUN chmod +x boot.sh

# Copy sources
COPY src/users_service.py app.py
COPY src/tracer.py tracer.py
COPY src/websockets_instrumentor.py websockets_instrumentor.py

EXPOSE ${HTTP_LISTEN_PORT}
ENTRYPOINT ["./boot.sh"]