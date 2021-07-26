from src.core import exceptions


class ErrorToSendResetPasswordEmail(exceptions.ServerException):
    """Raised when the reset password email fails"""

    def __init__(self):
        super().__init__("error to send email, please try again")


class InvalidAuthPayload(exceptions.ServerException):
    """Raised when the register payload it's invalid"""

    def __init__(self):
        super().__init__("invalid request payload")


class InvalidPayload(exceptions.ServerException):
    """Raised when the request payload it's invalid"""

    def __init__(self):
        super().__init__("invalid request payload")


class UnknownUser(exceptions.ServerException):
    """Raised when the user email was not found on database"""

    def __init__(self):
        super().__init__("ukwnown user if the given email")


class InvalidToken(exceptions.ServerException):
    """Raised when the token email was not found on database"""

    def __init__(self):
        super().__init__(
            "the given token was invalid, please generate a new one"
        )


class TokenNotFound(exceptions.ServerException):
    """Raised when the request was not found the JWT token"""

    def __init__(self):
        super().__init__("the request not contains the JWT token")


class WrongCredentials(exceptions.ServerException):
    """Raised when the user's password was wrong"""

    def __init__(self):
        super().__init__("the given password was wrong")
