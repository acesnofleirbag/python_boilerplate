from __future__ import annotations

import typing as T

from src.contexts.standard.aggregates.auth.domain import model
from src.core.ports import mailer, repository, unit_of_work

fake_user = {"email": "test@mail.com", "password": "test", "username": "test"}


class FakeUserUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeUserRepository()
        self.committed = False

    def rollback(self):
        pass

    def _commit(self):
        self.committed = True

    def collect_new_events(self) -> T.Generator:
        for user in self.users.seen:
            while user._events:
                yield user._events.pop(0)


class FakeUserRepository(repository.AbstractRepository):
    def __init__(self):
        super().__init__()
        self.database = []

    def _store(self, user: model.User):
        self.database.append(user)

    def _get(self, email: str) -> T.Optional[model.User]:
        try:
            return next(filter(lambda user: user.email == email, self.database))
        except StopIteration:
            return None

    def _update(self, id: str, payload: T.Dict):
        user = self._get(id)

        for k, v in payload.items():
            user.__dict__[k] = v

    def _destroy(self, email: str):
        self.database = [user for user in self.database if user.email != email]


class FakeMailer(mailer.AbstractMailer):
    sent: bool

    def __init__(self):
        self.sent = False

    def send(self):
        self.sent = True

        return 250
