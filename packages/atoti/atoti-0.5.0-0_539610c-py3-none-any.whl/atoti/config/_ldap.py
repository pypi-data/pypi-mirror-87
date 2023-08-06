from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping, Optional

from ._auth import Auth

LDAP_AUTH_TYPE = "ldap"


@dataclass(frozen=True)
class LdapAuthentication(Auth):
    """LDAP authentication."""

    url: str
    base_dn: str
    user_search_filter: Optional[str] = "(uid={0})"
    user_search_base: Optional[str] = ""
    group_search_filter: Optional[str] = "(uniqueMember={0})"
    group_search_base: Optional[str] = ""
    group_role_attribute_name: Optional[str] = "cn"
    role_mapping: Optional[Mapping[str, Collection[str]]] = None

    @property
    def _type(self):
        return LDAP_AUTH_TYPE

    @classmethod
    def _create(cls, data: Mapping[str, Any]) -> LdapAuthentication:
        return create_ldap_authentication(**data)


def create_ldap_authentication(
    *,
    url: str,
    base_dn: str,
    user_search_filter: str = "(uid={0})",
    user_search_base: str = "",
    group_search_filter: str = "(uniqueMember={0})",
    group_search_base: str = "",
    group_role_attribute_name: str = "cn",
    role_mapping: Optional[Mapping[str, Collection[str]]] = None
) -> LdapAuthentication:
    """Create a LDAP authentication.

    Args:
        url: The LDAP URL including the protocol and port.
            For instance ``ldap://example.com:389``.
        base_dn: Base Distinguished Name of the directory service.
            For instance ``dc=example,dc=com``.
        user_search_filter: The LDAP filter used to search for users.
            For instance ``(uid={0})``.
            The substituted parameter is the user's login name.
        user_search_base: Search base for user searches.
            For instance ``ou=people``
        group_search_filter: The LDAP filter to search for groups.
            For instance ``(uniqueMember={0})``.
            The substituted parameter is the DN of the user.
        group_search_base: The search base for group membership searches.
            For instance ``ou=roles``.
        group_role_attribute_name: The attribute name that maps a group to a role.
        role_mapping: The mapping between the roles returned by the LDAP authentication provider and the corresponding roles to use in atoti.
            LDAP roles are case insensitive.
            Users without the role ``ROLE_USER`` will not have access to the application.
    """
    return LdapAuthentication(
        url,
        base_dn,
        user_search_filter,
        user_search_base,
        group_search_filter,
        group_search_base,
        group_role_attribute_name,
        role_mapping,
    )
