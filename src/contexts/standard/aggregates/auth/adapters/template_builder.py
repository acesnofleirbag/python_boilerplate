import os
import pathlib
import string

from src.core.ports import template_builder


class ResetpassTemplateBuilder(template_builder.AbstractTemplateBuilder):
    def __init__(self):
        with open(
            pathlib.Path(
                "src/contexts/standard/aggregates/auth/services/mail/_templates/reset_password.html"
            )
        ) as file:
            self.template = file.read()

    def gentemplate(self, username: str, token: str):
        environments = dict(
            username=username,
            token=token,
            company=os.environ.get("APP_NAME", "PythonBoilerplate"),
        )

        email = string.Template(self.template).substitute(**environments)

        return email
