# PYTHON BOILERPLATE

Modular, transparent, fast web server with an isolated business layer with an
imperative decoupled core, to serve as a scaffold personal projects

### Features

- Fast ASGI server via `uvicorn`
- GraphQL support via `ariadne`
- JWT authentication
- Efficient dependency management via `poetry`
- Database migration system using `alembic`
- Event-driven architecture:
   - Internal message bus that injects dependencies into service-handlers
     functions
- Sober test pyramid: units, integrations and e2e tests
- Decoupled service layer that responds only to commands and events
- Aggregate's atomic services consistency guaranteed using `postgres` isolation
  levels locks
- Isolated and pure domain layer that has no dependencies - not even with ORM

### Instructions

For implementation instructions consult the `docs` folder

### Inspiration

I don't claim to have created everything from scratch. Quite the opposite, the
work here is a direct fork from another resources:

- cosmicpython book
- domain driven design
- hexagonal architecture
- solid
- and others

### TODO

- [ ] `i18n` support
- [ ] graphql support `ariadne`
- [ ] either nomad for error handling
- [ ] change endpoints to starlette - asynchronous
- [ ] reset token approach
- [ ] test pyramid

### Author

@thebe111
