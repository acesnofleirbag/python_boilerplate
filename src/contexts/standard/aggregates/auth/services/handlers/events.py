from src.contexts.standard.aggregates.auth.adapters import (
    mailer,
    template_builder,
)
from src.contexts.standard.aggregates.auth.domain import messages


def send_reset_password_email_token(
    message: messages.SendResetPasswordEmailToken,
    mailer: mailer.Mailer,
    template_builder: template_builder.ResetpassTemplateBuilder,
):
    mailer.send(
        email=message.payload["email"],
        subject="Reset Password",
        message=template_builder.gentemplate(
            message.payload["token"], message.payload["username"]
        ),
    )
