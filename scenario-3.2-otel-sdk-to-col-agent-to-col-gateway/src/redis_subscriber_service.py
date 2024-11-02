import json
import os
from opentelemetry.propagate import extract
from tracer import init_tracer

import redis

REDIS_URI = os.getenv("REDIS_URI", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
DECODE_UTF8 = "utf-8"
METRICS_PORT = int(os.getenv("METRICS_PORT", 9000))
SIGNALS_ENDPOINT = os.getenv("SIGNALS_ENDPOINT")


meter, tracer = init_tracer(
    service_name="redis_subscriber_service",
    signals_endpoint=SIGNALS_ENDPOINT
)


print("Initiating connection to Redis")
client = redis.Redis(host=REDIS_URI, port=REDIS_PORT)
print("Connection to Redis established")


def message_handler(message):
    message_data = message['data'].decode(DECODE_UTF8)
    channel = message['channel'].decode(DECODE_UTF8)
    
    payload = json.loads(message_data)

    propagated_context = extract(carrier=payload)

    with tracer.start_as_current_span("redis_message_consume", context=propagated_context, attributes=payload):
        print(f"Received {message} from {channel}")


pubsub = client.pubsub()
pubsub.subscribe(**{"my-channel": message_handler})


def main():
    try:
        for message in pubsub.listen():
            if message and message["type"] == "message":
                message_handler(message)
    except KeyboardInterrupt:
        print("Subscriber terminated")


if __name__ == "__main__":
    print("Running main")
    main()
