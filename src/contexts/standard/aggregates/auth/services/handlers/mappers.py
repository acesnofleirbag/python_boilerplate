from src.contexts.standard.aggregates.auth.domain import messages
from src.contexts.standard.aggregates.auth.services.handlers import command
from src.contexts.standard.aggregates.auth.services.handlers import (
    events as events_handler,
)
from src.contexts.standard.aggregates.auth.services.handlers import query

EVENT_HANDLERS = {
    messages.SendResetPasswordEmailToken: [
        events_handler.send_reset_password_email_token
    ]
}

COMMAND_HANDLERS = {
    messages.StoreRegister: command.store,
    messages.UpdateRegister: command.update,
    messages.DestroyRegister: command.destroy,
    messages.Login: command.login,
    messages.GenerateResetPasswordToken: command.generate_reset_password_token,
}
