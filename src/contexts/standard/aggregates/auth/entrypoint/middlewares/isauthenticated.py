import functools
import os
import typing as T

import jwt
from flask import request

from src.contexts.standard.aggregates.auth.domain import (
    exceptions as _exceptions,
)
from src.core import exceptions


def middleware(func):
    @functools.wraps(func)
    def wrapper(*args: T.Any, **kwargs: T.Dict[T.Any, T.Any]):
        try:
            authorization = None

            if "Authorization" in request.headers:
                authorization = request.headers.get("Authorization")

            if not authorization:
                raise _exceptions.TokenNotFound()

            if not "Bearer" in authorization:
                raise _exceptions.InvalidToken()

            try:
                token = authorization.replace("Bearer ", "")

                payload = jwt.decode(
                    token,
                    os.environ.get("JWT_SECRET_KEY", ""),
                    algorithms=[os.environ.get("JWT_ALGORITHM", "HS256")],
                )
            except jwt.InvalidTokenError as e:
                raise _exceptions.InvalidToken()

            return func(decoded_token=payload, *args, **kwargs)
        except Exception as e:
            return exceptions.resolver(e)

    return wrapper
