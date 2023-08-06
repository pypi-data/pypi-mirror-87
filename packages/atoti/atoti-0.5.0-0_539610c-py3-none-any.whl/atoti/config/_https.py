from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Union

from ._utils import Configuration


@dataclass(frozen=True)
class HttpsConfiguration(Configuration):

    certificate: Union[Path, str]
    password: str

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_https_config(**data)


def create_https_config(
    *, certificate: Union[Path, str], password: str
) -> HttpsConfiguration:
    """Create a PKCS 12 keystore configuration.

    Args:
        certificate: The path to the certificate
        password: The password for the certificate
    """
    return HttpsConfiguration(certificate=certificate, password=password)
