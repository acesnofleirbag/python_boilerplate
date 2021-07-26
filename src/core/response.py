import typing as T


class ServerResponse:
    data: T.Optional[T.Dict[str, object]]
    message: T.Optional[str]
    status_code: int

    def __init__(
        self,
        status_code: int = 200,
        message: T.Optional[str] = None,
        *,
        data: T.Optional[T.Dict[str, object]] = None
    ):
        self.status_code = status_code
        self.message = message
        self.data = data

    @property
    def payload(self):
        payload = dict(
            error=True if self.message else False,
            message=self.message,
            payload=self.data,
        )

        return payload
