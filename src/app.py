from fastapi import FastAPI,HTTPException,Header, Depends, status,Cookie,Request

from typing import Annotated

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from pydantic import BaseModel


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = ["http://127.0.0.1:8000"]

app.add_middleware(
   CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    disabled: bool


class CommonHeaders(BaseModel):
    Authorization: Annotated[str, Header()]
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


class Cookies(BaseModel):
    session_id: str | None = None
    token: str | None = None

users = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "z1G8C@example.com"
    },
    {
        "id": 2,
        "name": "Jane Doe",
        "email": "z1G8C@example.com"
    },
    {
        "id": 3,
        "name": "John Doe",
        "email": "z1G8C@example.com"
    }
]


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users", response_model=list[User], tags=["users"], summary="Get list of users", description="Get list of users", response_description="List of users", status_code=200)
def get_users():
    return users

@app.get("/users/{user_id}", response_model=User, tags=["users"], summary="Get user by ID", description="Get user by ID", response_description="User", status_code=200)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return JSONResponse(status_code=200, content=user)
    raise HTTPException(status_code=404, detail={"message": "User not found"})

@app.post("/singup", tags=["auth"], summary="Create new user", description="Create new user", response_description="User", status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.model_dump()}, expires_delta=access_token_expires
    )

    # {**user, "token": token}
    # users.append(user)
    # return JSONResponse(status_code=201, content={"user": user.model_dump(), "token": access_token})   
    return {"user": user, "token": access_token}


@app.get("/cookies", tags=["cookies"], summary="Get cookies", description="Get cookies", response_description="Cookies", status_code=200)
def get_cookies(res:Request):
    return {"cookies": res.cookies}