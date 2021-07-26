AUTH_PAYLOAD = {
    "email": {
        "type": "string",
        "required": True,
        "maxlength": 255,
        "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "coerce": "strnormalize",
    },
    "password": {"type": "string", "required": True},
    "username": {
        "type": "string",
        "required": True,
        "maxlength": 100,
        "coerce": "strnormalize",
    },
}

UPDATE_AUTH_PAYLOAD = {
    "email": {
        "type": "string",
        "required": False,
        "nullable": True,
        "maxlength": 255,
        "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "coerce": "strnormalize",
    },
    "password": {"type": "string", "required": False, "nullable": True},
    "username": {
        "type": "string",
        "required": False,
        "nullable": True,
        "maxlength": 100,
        "coerce": "strnormalize",
    },
}
