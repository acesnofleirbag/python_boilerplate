from src.contexts.standard.aggregates.auth.domain import (
    exceptions,
    messages,
    model,
)
from src.core.ports import unit_of_work


def store(
    message: messages.StoreRegister, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        user = model.User(
            message.payload["email"],
            message.payload["password"],
            message.payload["username"],
        )

        uow.users.store(user)
        uow.commit()


def update(
    message: messages.UpdateRegister, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        user = uow.users.get(message.decoded_token["sub"])

        uow.users.update(user.email, message.payload)
        uow.commit()


def destroy(
    message: messages.DestroyRegister, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        uow.users.destroy(message.id_user)
        uow.commit()


def login(message: messages.Login, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        user = uow.users.get(message.payload["email"])

        if not user:
            raise exceptions.UnknownUser()

        if not user.checkpass(message.payload["password"]):
            raise exceptions.WrongCredentials()

        return user.gentoken()


def generate_reset_password_token(
    message: messages.GenerateResetPasswordToken,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(message.payload["email"])

        if not user:
            raise exceptions.UnknownUser()

        user.generate_reset_password_token()
