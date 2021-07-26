import abc
import typing as T

from sqlalchemy import orm

from src.core import domain


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: T.Set[domain.Aggregate] = set()

    def store(self, aggregate: domain.Aggregate) -> None:
        self.seen.add(aggregate)
        self._store(aggregate)

    def get(self, id: str) -> domain.Aggregate:
        aggregate = self._get(id)

        if aggregate:
            self.seen.add(aggregate)

        return aggregate

    def update(self, id: str, payload: T.Dict) -> None:
        aggregate = self._get(id)

        if aggregate:
            self.seen.add(aggregate)

        self._update(id, payload)

    def destroy(self, id: str) -> None:
        aggregate = self._get(id)

        if aggregate:
            self.seen.add(aggregate)
            self._destroy(id)

    @abc.abstractmethod
    def _store(self, aggregate: domain.Aggregate) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: str) -> domain.Aggregate:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, id: str, payload: T.Dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _destroy(self, id: str) -> None:
        raise NotImplementedError


class AbstractSqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: orm.Session):
        self.session = session
        super().__init__()

    @abc.abstractmethod
    def _store(self, aggregate: domain.Aggregate) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, id: str) -> domain.Aggregate:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, id: str, payload: T.Dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _destroy(self, id: str) -> None:
        raise NotImplementedError
