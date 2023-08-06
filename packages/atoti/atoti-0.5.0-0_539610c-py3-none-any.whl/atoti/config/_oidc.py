from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping, Optional

from ._auth import Auth

OIDC_AUTH_TYPE = "oidc"


@dataclass(frozen=True)
class OidcAuthentication(Auth):
    """OpenID connect authentication."""

    provider_id: str
    issuer_url: str
    client_id: str
    client_secret: str
    name_attribute: Optional[str]
    paths_to_authorities: Optional[Collection[str]]
    scopes: Optional[Collection[str]]
    role_mapping: Optional[Mapping[str, Collection[str]]]

    @property
    def _type(self):
        return OIDC_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_oidc_authentication(**data)


def create_oidc_authentication(
    *,
    provider_id: str,
    issuer_url: str,
    client_id: str,
    client_secret: str,
    name_attribute: Optional[str] = None,
    paths_to_authorities: Optional[Collection[str]] = None,
    scopes: Optional[Collection[str]] = None,
    role_mapping: Optional[Mapping[str, Collection[str]]] = None,
) -> OidcAuthentication:
    """Create an OpenID connect authentication.

    Args:
        provider_id: The name of your provider.
            This string is used to build the ``redirectUrl`` using this template ``{baseUrl}:{port}/login/oauth2/code/{providerId}`` .
        issuer_url: The issuer URL parameter from your provider's OpenID connect configuration endpoint.
        client_id: The app's ``clientId``, obtained from the authentication provider.
        client_secret: The app's ``clientSecret``, obtained from the authentication provider.
        name_attribute: The key in the ``idToken`` of the parameter to display as the username in the application.
        paths_to_authorities: The path to the authorities to use in atoti in the returned access token or id token.
        scopes: The scopes to request from the authentication provider (e.g. email, username, etc.).
        role_mapping: The mapping between the roles returned by the authentication provider and the corresponding roles to use in atoti.
            Users without the role ``ROLE_USER`` will not have access to the application.
    """
    return OidcAuthentication(
        provider_id,
        issuer_url,
        client_id,
        client_secret,
        name_attribute,
        paths_to_authorities,
        scopes,
        role_mapping if role_mapping is not None else {},
    )
