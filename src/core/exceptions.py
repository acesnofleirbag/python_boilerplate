from __future__ import annotations

import functools
import os
import typing as T

from src.core import response

APP_NAME = os.environ.get("APP_NAME", "ERROR")


def handle_exception(
    func,
) -> T.Callable[[str], T.Tuple[T.Dict[str, object], int]]:
    @functools.wraps(func)
    def wrapper(exception):
        message, error_type = func(exception)

        res = response.ServerResponse(
            status_code=500 if error_type == "UnknownError" else 404,
            message=message,
        )

        return res.payload, res.status_code

    return wrapper


@handle_exception
def resolver(exception) -> T.Tuple[str, str]:
    if isinstance(exception, ServerException):
        return exception.message, str(exception.__class__.__name__)
    else:
        return UnknownError().message, "UnkwnownError"


class ServerException(Exception):
    """
    Base server exception

    Attributes:
        - messsage: exception's message to shows on HTTP response
    """

    message: str

    def __init__(self, message: str):
        self.message = message


class UnknownError(ServerException):
    """Raised when any other non-mapped exception was given"""

    def __init__(self):
        super().__init__("unknown error")


class UnknownMessage(ServerException):
    """Raised when the message type was not recognized"""

    def __init__(self):
        super().__init__("unknown message with the given category")
