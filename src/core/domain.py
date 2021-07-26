import abc
import datetime
import typing as T


class Aggregate:
    _events: T.List
    _version: int

    def __init__(self):
        self._events = []
        self._version = 0


class Entity(Aggregate):
    def __init__(self):
        super().__init__()


class ValueObject(Aggregate):
    def __init__(self):
        super().__init__()


class Message:
    kind: str
    raised_at: datetime.datetime

    def __init__(self):
        self.type = "GenericMessage"
        self.kind = self.__class__.__name__
        self.raised_at = datetime.datetime.now()
        self.delay = 0

    def __str__(self) -> str:
        return str(self.__repr__())

    def __repr__(self) -> str:
        return (
            f"<({self.type} - {self.kind}) raised at: {self.raised_at}"
            f"with params: {self.__dict__}>"
        )


class Event(Message):
    def __init__(self):
        super().__init__()
        self.type = "Event"


class Command(Message):
    def __init__(self):
        super().__init__()
        self.type = "Command"


class Query(Message):
    def __init__(self):
        super().__init__()
        self.type = "query"
