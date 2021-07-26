import inspect
import typing as T

import cerberus

from src.core import domain


def inject_dependencies(handler, dependencies) -> T.Any:
    """
    Called in the bootstrap aggregate to inject handlers dependencies

    Arguments:
        - handler (callable): the message handler
        - dependencies (dict): the handler dependecies

    Returns:
        any: returns a message handler
    """

    params = inspect.signature(handler).parameters

    _dependencies = {
        arg: dependency
        for arg, dependency in dependencies.items()
        if arg in params
    }

    return lambda message: handler(message, **_dependencies)


class ServerValidator(cerberus.Validator):
    """
    Custom server validator if extends the cerberus validator class

    Methods:
        - coerce: coerce overwritten
          - strnormalize: return the given value in the lowercase
    """

    def _normalize_coerce_strnormalize(self, payload: str) -> str:
        """
        Called when the data as a string and need to be normalized

        Arguments:
            - value (str): the payload given value

        Returns:
            str: a normalized (lowercase) string value
        """

        return payload.lower()
