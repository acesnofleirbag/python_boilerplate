from __future__ import annotations

import abc
import typing as T

from sqlalchemy import orm

from src.contexts.entrypoint import orm as _orm


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> T.Any:
        return self

    def __exit__(self, *args: T.Any) -> None:
        self.rollback()

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        self._commit()
        self.collect_new_events()

    @abc.abstractmethod
    def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def collect_new_events(self) -> T.Generator:
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    session: orm.Session

    def __init__(
        self, session_factory: T.Callable = _orm.DEFAULT_SESSION_FACTORY
    ):
        self.session_factory = session_factory

    def __exit__(self, *args: T.Any):
        super().__exit__(*args)
        self.session.close()

    def _commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
