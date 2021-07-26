from flask import Blueprint, Flask

from src.contexts.entrypoint import config


def create_app(cfg=config):
    app = Flask(__name__)
    app.config.from_object(cfg.Config)

    with app.app_context():
        from src.contexts.standard.aggregates.auth.entrypoint.rest import (
            routes as auth,
        )

        app.register_blueprint(auth.router)

    return app
