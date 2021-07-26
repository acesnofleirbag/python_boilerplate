from src.contexts.entrypoint import orm
from src.contexts.standard.aggregates.auth import bootstrap as auth


def boot(start_orm=True):
    if start_orm:
        orm.start_mappers()
