from faker import Faker
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()
fake = Faker()
MAX_LEN = 100


def generate_users():
    users = []
    for _ in range(0, MAX_LEN):
        user = {
            "username": fake.user_name(),
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "emailAddress": fake.email(),
        }
        users.append(user)
    return users


users = generate_users()


@app.get("/get_users")
def get_users():
    return JSONResponse(generate_users())
