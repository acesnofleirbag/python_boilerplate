from src.contexts.entrypoint import orm
from src.contexts.standard.aggregates.auth.adapters import (
    mailer,
    template_builder,
)
from src.contexts.standard.aggregates.auth.services import unit_of_work
from src.contexts.standard.aggregates.auth.services.handlers import mappers
from src.core import helpers, messagebus


def boot(
    start_orm=False,
    uow=unit_of_work.AuthSQLAlchemyUnitOfWork(),
    mailer=mailer.Mailer(),
    template_builder=template_builder.ResetpassTemplateBuilder(),
):
    dependencies = dict(
        uow=uow, mailer=mailer, template_builder=template_builder
    )

    injected_event_handlers = {
        _type: [
            helpers.inject_dependencies(handler, dependencies)
            for handler in handlers
        ]
        for _type, handlers in mappers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        _type: helpers.inject_dependencies(handler, dependencies)
        for _type, handler in mappers.COMMAND_HANDLERS.items()
    }

    _messagebus = messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )

    return _messagebus
