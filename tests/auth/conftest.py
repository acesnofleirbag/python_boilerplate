import os

import jwt
import pytest

from src.contexts.standard.aggregates.auth import bootstrap
from src.contexts.standard.aggregates.auth.domain import model
from src.contexts.standard.aggregates.auth.services import unit_of_work
from tests.fakes import auth


@pytest.fixture
def fake_messagebus():
    uow = auth.FakeUserUnitOfWork()
    mailer = auth.FakeMailer()
    template_builder = None

    yield bootstrap.boot(
        uow=uow, mailer=mailer, template_builder=template_builder
    )


@pytest.fixture
def uow():
    uow = unit_of_work.AuthSQLAlchemyUnitOfWork()

    return uow


@pytest.fixture
def decoded_token():
    token = model.User(**auth.fake_user).gentoken()

    yield jwt.decode(
        token,
        os.environ.get("JWT_SECRET_KEY", ""),
        algorithms=[os.environ.get("JWT_ALGORITHM", "HS256")],
        options={"verify_signature": False},
    )
