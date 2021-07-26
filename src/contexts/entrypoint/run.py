from src.contexts.entrypoint import app as factory
from src.contexts.entrypoint import bootstrap

app = factory.create_app()
bootstrap.boot()

if __name__ == "__main__":
    app.run()
