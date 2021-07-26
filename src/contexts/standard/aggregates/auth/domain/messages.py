import typing as T

from src.contexts.standard.aggregates.auth.adapters import mailer
from src.contexts.standard.aggregates.auth.domain import exceptions, validations
from src.core import domain, helpers


class SendResetPasswordEmailToken(domain.Event):
    def __init__(self, email: str, username: str, token: str):
        super().__init__()

        self.payload = dict(email=email, username=username, token=token)


class GenerateResetPasswordToken(domain.Command):
    """
    Called when a user request a reset password

    Attributes:
        - payload (dict): payload's attributes description
          - email (str): outgoing user's email
    """

    payload: T.Dict[str, str]

    def __init__(self, email: str):
        super().__init__()

        data = dict(email=email)
        validator = helpers.ServerValidator(
            {
                "email": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                    "maxlength": 255,
                    "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                    "coerce": "strnormalize",
                }
            }
        )

        if not (validator.validate(data)):
            raise exceptions.InvalidPayload()

        self.payload = validator.normalized(data)


class StoreRegister(domain.Command):
    """
    Called when a user request a register

    Attributes:
        - payload (dict): message's payload
          - email (str): user's email
          - password (str): user's non-encrypted password
          - username (str): user's username

    Exceptions:
        - InvalidAuthPayload: raised when a payload contains validations errors
    """

    payload: T.Dict[str, str]

    def __init__(self, email: str, password: str, username: str):
        super().__init__()

        data = dict(email=email, password=password, username=username)
        validator = helpers.ServerValidator(validations.AUTH_PAYLOAD)

        if not (validator.validate(data)):
            raise exceptions.InvalidAuthPayload()

        self.payload = validator.normalized(data)


class UpdateRegister(domain.Command):
    """
    Called when the user request a update register

    Attributes:
        - decoded_token (dict): the user's request token payload
        - payload (dict): message's payload
          - email (str, optional): user's updated email
          - password (str, optional): user's updated password
          - username (str, optional): user's updated username

    Exceptions:
        - InvalidAuthPayload: raised when a payload contains validations errors
    """

    payload: T.Dict[str, str]
    decoded_token: T.Dict

    def __init__(
        self,
        email: str = None,
        password: str = None,
        username: str = None,
        *,
        decoded_token: T.Dict
    ):
        super().__init__()

        self.decoded_token = decoded_token

        data = dict(email=email, password=password, username=username)
        validator = helpers.ServerValidator(validations.UPDATE_AUTH_PAYLOAD)

        if not (validator.validate(data)):
            raise exceptions.InvalidAuthPayload()

        self.payload = {
            k: v for k, v in validator.normalized(data).items() if v is not None
        }


class DestroyRegister(domain.Command):
    """
    Called when the user request an account deletion

    Attributes:
        - id_user: user's ID fro deletion
    """

    id_user: str

    def __init__(self, id_user: str):
        super().__init__()

        self.id_user = id_user


class Login(domain.Command):
    """
    Called when the user makes login

    Attributes:
        - payload (dict): payload's attributes description
          - email (str): user's email
          - password (str): user's password
    """

    payload: T.Dict[str, str]

    def __init__(self, email: str, password: str):
        super().__init__()

        self.payload = dict(email=email, password=password)
