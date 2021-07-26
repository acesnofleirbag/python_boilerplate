import typing as T

from src.contexts.standard.aggregates.auth.adapters import repository
from src.core.ports import unit_of_work


class AuthSQLAlchemyUnitOfWork(unit_of_work.SQLAlchemyUnitOfWork):
    def __enter__(self):
        self.session = self.session_factory()
        self.users = repository.UserSQLAlchemyRepository(self.session)

        return super().__enter__()

    def collect_new_events(self) -> T.Generator:
        for aggregate in self.users.seen:
            while aggregate._events:
                yield aggregate._events.pop(0)
