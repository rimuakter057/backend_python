from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/my-name")
def my_name():
    return {"name": "John Doe"}

# Signup request body
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


@app.post("/signup")
def signup(data: SignupRequest):
    return {
        "message": "Signup successful",
        "name": data.name,
        "email": data.email
    }