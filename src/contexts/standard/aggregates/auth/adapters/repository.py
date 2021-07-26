import typing as T

from src.contexts.standard.aggregates.auth.domain import model
from src.core.ports import repository


class UserSQLAlchemyRepository(repository.AbstractSqlAlchemyRepository):
    def __init__(self, session):
        super().__init__(session)

    def _store(self, user: model.User):
        self.session.add(user)

    def _get(self, email: str) -> model.User:
        return (
            self.session.query(model.User)
            .filter(model.User.email == email)
            .first()
        )

    def _update(self, id: str, payload: T.Dict):
        self.session.query(model.User).filter(model.User.email == id).update(
            payload
        )

    def _destroy(self, id: str):
        self.session.query(model.User).filter(id == id).update(
            {"deleted": True}
        )
