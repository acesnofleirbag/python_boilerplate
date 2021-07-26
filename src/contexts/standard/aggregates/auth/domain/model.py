import datetime
import os
import typing as T

import jwt
from passlib.context import CryptContext

from src.contexts.standard.aggregates.auth.domain import messages
from src.core import domain

crypter = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(domain.Entity):
    """
    User's account entity abstraction

    Attributes:
        - email (str): used to make login on system
        - password (str): used to make login on system
        - username (str): appears on dashboard if exists

    Methods:
        - hashpass: makes a password hash
        - checkpass: checks if the given password as the same as recorded in
          the database
        - changepass: makes a new hash for given password
        - generate_reset_password_token: generate a valid reset password token
    """

    email: str
    password: str
    username: str

    def __init__(self, email: str, password: str, username: str):
        self.email = email
        self.password = self.hashpass(password)
        self.username = username
        super().__init__()

    def __repr__(self) -> str:
        """
        Default user's __repr__
        """

        return f"<User {self.email}>"

    def __hash__(self) -> int:
        """
        Default user's __hash__
        """

        return hash(self.email)

    def __equal__(self, other: T.Any) -> bool:
        """
        Default user's __equal__
        """

        return isinstance(other, User) and other.email == self.email

    @staticmethod
    def hashpass(password: str) -> T.Any:
        """
        Called when the user makes a new register

        Arguments:
            - password: user's password to be hashed

        Returns:
            - any: the user's password in the bcrypt hash format
        """

        return crypter.hash(password)

    def checkpass(self, password: str) -> bool:
        """
        Called to when the user makes login

        Arguments:
            - password: user's password

        Returns:
            - bool: True if the password is the same, false otherwise
        """

        return bool(crypter.verify(password, self.password))

    def changepass(self, password: str) -> None:
        """
        Called when the user request a reset password

        Arguments:
            - password: user's new password
        """

        self.password = self.hashpass(password)

    def generate_reset_password_token(self) -> None:
        """
        Called when the user request a reset password

        Events:
            - GenerateResetPasswordToken
        """

        expiration: datetime.datetime = (
            datetime.datetime.utcnow()
            + datetime.timedelta(
                minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
            )
        )

        payload: T.Dict = dict(
            sub=self.password, exp=expiration, nbf=datetime.datetime.utcnow()
        )

        token = jwt.encode(
            payload=payload,
            key=os.environ.get(
                "JWT_SECRET_KEY", "1e047887edbc42c69d58e611254a4a21"
            ),
            algorithm=os.environ.get("JWT_ALGORITHM", "HS256"),
        )

        self._events.append(
            messages.SendResetPasswordEmailToken(
                self.email, self.username, token
            )
        )

    def gentoken(self) -> str:
        expiration: datetime.datetime = (
            datetime.datetime.utcnow()
            + datetime.timedelta(
                minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
            )
        )

        payload: T.Dict = dict(sub=self.email, exp=expiration)

        token = jwt.encode(
            payload=payload,
            key=os.environ.get(
                "JWT_SECRET_KEY", "1e047887edbc42c69d58e611254a4a21"
            ),
            algorithm=os.environ.get("JWT_ALGORITHM", "HS256"),
        )

        return token
