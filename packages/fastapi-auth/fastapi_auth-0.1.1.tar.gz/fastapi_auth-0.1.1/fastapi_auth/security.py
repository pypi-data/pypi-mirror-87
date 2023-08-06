from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from starlette.responses import Response, RedirectResponse

from backend.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

KEY = "Authorization"
ALGORITHM = "HS256"


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_cookie(token: str):
    response = Response()
    response.set_cookie(**get_token_data(token))
    return response


def create_cookie_with_redirect(path: str, token: str):
    response = RedirectResponse(path)
    response.set_cookie(**get_token_data(token))
    return response


def get_token_data(token: str):
    return dict(
        key=KEY,
        value=f"Bearer {token}",
        domain=settings.DOMAIN,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def delete_cookie():
    response = Response()

    response.delete_cookie(
        key=KEY,
        path='/',
        domain=settings.DOMAIN
    )

    return response


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

