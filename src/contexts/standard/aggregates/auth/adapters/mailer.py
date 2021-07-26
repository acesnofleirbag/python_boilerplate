import os

import emails

from src.contexts.standard.aggregates.auth.domain import exceptions
from src.core.ports import mailer


class Mailer(mailer.AbstractMailer):
    def __init__(self):
        super().__init__()

    def send(self, email: str, subject: str, message: str) -> None:
        server = emails.Message(
            subject=subject,
            html=message,
            mail_from=(self.user["name"], self.user["email"]),
        )

        response = server.send(to=email, smtp=self.settings)

        if response.status != 250:
            raise exceptions.ErrorToSendResetPasswordEmail()
