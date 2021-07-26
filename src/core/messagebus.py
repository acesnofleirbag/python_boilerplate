import typing as T

from src.core import domain, exceptions
from src.core.ports import unit_of_work


class MessageBus:
    """
    Message bus makes the workflow proccess mapping each message type for your
    specific handler

    Attributes:
        - uow (abstract uow): the aggregates specific uow
        - event_handlers (list): the aggregate's event handlers
        - command_handlers (list): the aggregate's command handlers
        - queue (list): the queue of messages to be processed

    Methods:
        - handle_mapper: called to makes relation between the message and your
          specific handler type
        - handle_event: called to execute a event handler with an event message
        - handle_command: called to execute a command handler with an command
          message
        - handle: called to execute a handler

    Exceptions:
        - UnkwnownMessage: raise when coming a unkwnown message type
    """

    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers,
        command_handlers,
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: T.List[domain.Message] = []

    def handle_event(self, event: domain.Event) -> None:
        """
        Called when an event was found in the queue message

        Arguments:
            - event: an event type message

        Exceptions:
            don't raises any exception because an event can fail, events was
            'optional' actions
        """

        for handler in self.event_handlers[type(event)]:
            try:
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception as e:
                continue

    def handle_command(self, command: domain.Command) -> None:
        """
        Called when a command was found in the queue message

        Arguments:
            - command: a command type message

        Exceptions:
            raise any type of error
        """

        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception as e:
            raise

    def handle_mapper(self, message: domain.Message) -> T.Callable:
        """
        Called to makes relation between the message and your specific mesage
        handler type

        Arguments:
            - message: a system messsage

        Exceptions:
            - UnknownMessage: raise when coming an unknown message type
        """
        if isinstance(message, domain.Event):
            return self.handle_event
        elif isinstance(message, domain.Command):
            return self.handle_command
        else:
            raise exceptions.UnknownMessage()

    def handle(self, message: domain.Message) -> T.Any:
        """
        Called to execute a handler

        Arguments:
            - message: a system message
        """
        self.queue = [message]

        while self.queue:
            task = self.queue.pop(0)
            handle = self.handle_mapper(task)

            handle(task)
