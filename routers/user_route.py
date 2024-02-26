from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from middlewares.jwt_bearer import create_token

user_route = APIRouter()


class User(BaseModel):
    email: str
    password: str


@user_route.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token: str = create_token(user.__dict__)
    return JSONResponse(token)
