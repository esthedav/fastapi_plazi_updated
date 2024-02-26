from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import encode, decode


def create_token(data: dict):
    token: str = encode(
        payload=data,
        key="secret_key",
        algorithm="HS256",
    )
    return token


def validate_token(token: str):
    data: dict = decode(token, key="secret_key", algorithms=["HS256"])
    return data


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@mail.com":
            raise HTTPException(status_code=403, detail="Invalid Credentials")
