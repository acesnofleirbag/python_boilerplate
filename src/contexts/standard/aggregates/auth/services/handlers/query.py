from src.contexts.standard.aggregates.auth.domain import exceptions
from src.core.ports import unit_of_work


def index():
    ...


def show(email: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.session.execute(
            """
            SELECT
                id,
                email,
                username
            FROM users
            WHERE deleted = false
            AND email = :email
            """,
            dict(email=email),
        ).fetchone()

        if not user:
            raise exceptions.UnknownUser()

        return dict(user)
