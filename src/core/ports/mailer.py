import abc
import os
import typing as T


class AbstractMailer(abc.ABC):
    def __init__(self):
        self.user: T.Dict = dict(
            name=os.environ.get("MAIL_FROM_NAME", ""),
            email=os.environ.get("MAIL_FROM_ADDRESS", ""),
        )

        self.settings: T.Dict = dict(
            host=os.environ.get("MAIL_HOST", "smtp.com"),
            port=int(os.environ.get("MAIL_PORT", 465)),
            user=os.environ.get("MAIL_USER", "user"),
            password=os.environ.get("MAIL_PASSWORD", "password"),
            tls=True,
        )

    @abc.abstractmethod
    def send(self):
        raise NotImplementedError
