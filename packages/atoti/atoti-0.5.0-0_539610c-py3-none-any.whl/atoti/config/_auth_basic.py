from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Collection, Mapping, Optional

from ._auth import Auth
from ._utils import Configuration

BASIC_AUTH_TYPE = "basic"
ROLE_USER = "ROLE_USER"


@dataclass(frozen=True)
class BasicUser(Configuration):
    """Basic user with roles."""

    name: str
    password: str
    roles: Collection[str] = field(default_factory=list)

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_basic_user(**data)


def create_basic_user(
    name: str, password: str, *, roles: Optional[Collection[str]] = None
) -> BasicUser:
    """Create a basic user with roles.

    Args:
        name: User name.
        password: User password.
        roles: The roles given to the user.
            The role ``ROLE_USER``, which is required to access the application, will automatically be added to the passed roles.
    """
    roles = set(roles) if roles is not None else set()
    roles.add(ROLE_USER)
    return BasicUser(name, password, roles)


@dataclass(frozen=True)
class BasicAuthentication(Auth):
    """Basic authentication."""

    users: Collection[BasicUser]
    realm: Optional[str] = None

    @property
    def _type(self):
        return BASIC_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]) -> BasicAuthentication:
        """Create the authentication from dictionary."""
        data_dict = dict(data)
        users_data = data_dict.pop("users")
        users = [BasicUser._from_dict(user) for user in users_data]
        return create_basic_authentication(users, **data_dict)


def create_basic_authentication(
    users: Collection[BasicUser], *, realm: Optional[str] = None
) -> BasicAuthentication:
    """Create a basic authentication.

    Args:
        users: The users that can authenticate against the session.
        realm: The realm describing the protected area.
            Different realms can be used to isolate sessions running on the same domain (regardless of the port).
            The realm will also be displayed by the browser when prompting for credentials.
            Defaults to ``f"{session_name} atoti session at {session_id}"``.

    """
    return BasicAuthentication(users, realm)
