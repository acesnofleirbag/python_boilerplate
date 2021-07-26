import os

from sqlalchemy import MetaData, create_engine, orm

from src.contexts.standard.aggregates.auth.adapters import orm as auth

_DATABASE_URI = (
    os.environ.get("DATABASE_URI", "sqlite:///development.sqlite3")
    if os.environ.get("ENVIRONMENT", "DEVELOPMENT").lower() == "production"
    else "sqlite:///development.sqlite3"
)

DEFAULT_SESSION_FACTORY: orm.Session = orm.sessionmaker(
    # NOTE(database): isolation level ensures aggregate's version is respected
    # ---
    # FONT: <https://www.postgresql.org/docs/current/transaction-iso.html> -
    # more details about isolation levels
    bind=create_engine(
        _DATABASE_URI,
        #  isolation_level="REPEATABLE_READ"
    ),
    autoflush=False,
)


def start_mappers():
    metadata = MetaData()

    auth.start_mappers(metadata)

    return metadata
