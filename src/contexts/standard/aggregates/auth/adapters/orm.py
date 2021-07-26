import typing as T
import uuid
from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    MetaData,
    String,
    Table,
    Text,
    orm,
)

from src.contexts.standard.aggregates.auth.domain import model

users: T.Callable[[MetaData], Table] = lambda metadata: Table(
    "users",
    metadata,
    Column(
        "id",
        String(64),
        primary_key=True,
        nullable=False,
        unique=True,
        default=lambda: str(uuid.uuid4()),
    ),
    Column("email", String(255), nullable=False, unique=True),
    Column("password", Text, nullable=False),
    Column("username", String(100), nullable=False),
    Column(
        "created_at",
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.today(),
    ),
    Column(
        "updated_at",
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.today(),
        onupdate=lambda: datetime.today(),
    ),
    Column("deleted", Boolean(), nullable=False, default=False),
)


def start_mappers(metadata):
    orm.mapper(model.User, users(metadata))


@orm.events.event.listens_for(model.User, "load")
def dynamic_attributes(aggregate, _: T.Any) -> None:
    """
    Note: it's necessary to generate the mapper _events attribute
    """

    aggregate._events = []
