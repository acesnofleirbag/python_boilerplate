import os

from flask import Blueprint, request

from src.contexts.standard.aggregates.auth import bootstrap
from src.contexts.standard.aggregates.auth.domain import exceptions, messages
from src.contexts.standard.aggregates.auth.entrypoint.middlewares.isauthenticated import (
    middleware as _isauthenticated,
)
from src.contexts.standard.aggregates.auth.services import unit_of_work
from src.contexts.standard.aggregates.auth.services.handlers import (
    command,
    query,
)
from src.core import exceptions, response

router = Blueprint("router", __name__)

_messagebus = bootstrap.boot()


@router.route("/auth/store", methods=["POST"])
def store():
    payload = request.json

    try:
        _messagebus.handle(messages.StoreRegister(**payload))
    except Exception as e:
        return exceptions.resolver(e)

    res = response.ServerResponse(201)

    return res.payload, res.status_code


@router.route("/auth/show", methods=["GET"])
@_isauthenticated
def show(decoded_token):
    try:
        payload = query.show(decoded_token["sub"], _messagebus.uow)
    except Exception as e:
        return exceptions.resolver(e)

    res = response.ServerResponse(data=payload)

    return res.payload, res.status_code


@router.route("/auth/update", methods=["PUT"])
@_isauthenticated
def update(decoded_token):
    payload = request.json

    try:
        _messagebus.handle(
            messages.UpdateRegister(**payload, decoded_token=decoded_token)
        )
    except Exception as e:
        return exceptions.resolver(e)

    res = response.ServerResponse()

    return res.payload, res.status_code


@router.route("/auth/destroy", methods=["DELETE"])
@_isauthenticated
def destroy(decoded_token):
    raise NotImplementedError


@router.route("/auth/login", methods=["POST"])
def login():
    payload = request.json

    try:
        token = command.login(messages.Login(**payload), _messagebus.uow)
    except Exception as e:
        return exceptions.resolver(e)

    res = response.ServerResponse(data=token)

    return res.payload, res.status_code


@router.route("/auth/resetpass", methods=["PATCH"])
def resetpass():
    payload = request.json

    try:
        _messagebus.handle(messages.GenerateResetPasswordToken(**payload))
    except Exception as e:
        return exceptions.resolver(e)

    res = response.ServerResponse()

    return res.payload, res.status_code
