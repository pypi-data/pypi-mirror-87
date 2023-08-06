from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Any, Mapping

from ._utils import Configuration


def is_base64(value: str) -> bool:
    """Check if a string is base64 encoded."""
    try:
        return base64.b64encode(base64.b64decode(value)).decode("ascii") == value
    except Exception:  # pylint: disable=broad-except
        return False


def get_base64_encoded(value: str) -> str:
    """Get the base64 encoded string."""
    if is_base64(value):
        return value

    return base64.b64encode(value.encode("ascii")).decode("ascii")


@dataclass(frozen=True)
class JwtKeyPair(Configuration):

    public_key: str
    private_key: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_jwt_key_pair(**data)


def create_jwt_key_pair(public_key: str, private_key: str) -> JwtKeyPair:
    """Return a key pair to sign JSON Web Tokens.

    Only RSA keys using the PKCS 8 standard are supported.
    A key pair can be generated using a library like ``pycryptodome`` for example.
    """
    public_key = get_base64_encoded(public_key)
    private_key = get_base64_encoded(private_key)
    return JwtKeyPair(public_key=public_key, private_key=private_key)
