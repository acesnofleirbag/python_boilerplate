import faker
import pytest

from src.contexts.standard.aggregates.auth.domain import messages
from tests.fakes import auth

fake = faker.Faker()


def test_if_the_user_was_storaged(fake_messagebus):
    _messagebus = fake_messagebus
    message = messages.StoreRegister(**auth.fake_user)

    _messagebus.handle(message)

    assert _messagebus.uow.users.get("test@mail.com")


def test_if_the_user_username_was_updated(fake_messagebus, decoded_token):
    _messagebus = fake_messagebus
    payload = auth.fake_user
    payload.update(username="bart")

    message_queue = [
        messages.StoreRegister(**auth.fake_user),
        messages.UpdateRegister(**payload, decoded_token=decoded_token),
    ]

    [_messagebus.handle(message) for message in message_queue]

    assert _messagebus.uow.users.get("test@mail.com").username == "bart"


def test_if_the_user_is_removed(fake_messagebus, decoded_token):
    _messagebus = fake_messagebus

    message_queue = [
        messages.StoreRegister(**auth.fake_user),
        messages.DestroyRegister(decoded_token["sub"]),
    ]

    [_messagebus.handle(message) for message in message_queue]

    assert len(_messagebus.uow.users.database) == 0
