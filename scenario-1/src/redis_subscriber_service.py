import redis
import json
import time
import os

REDIS_URI = os.getenv("REDIS_URI", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

print("Initiating connection to Redis")
client = redis.Redis(host=REDIS_URI, port=REDIS_PORT)
print("Connection to Redis established")


def message_handler(message):
    _ = json.loads(message['data'])
    print(f"Received {message['data']} from {message['channel']}")

pubsub = client.pubsub()
pubsub.subscribe(**{'my-channel': message_handler})

def main():
    try:
        while True:
            print("Waiting for message")
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                message_handler(message)
            time.sleep(0.02)
    except KeyboardInterrupt:
        print ("Subscriber terminated")

if __name__ == "__main__":
    print("Running main")
    main()
