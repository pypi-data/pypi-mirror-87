from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, Mapping, Optional, Union

from ._utils import Configuration

Restrictions = Mapping[str, Union[str, Collection[str]]]


@dataclass(frozen=True)
class Role(Configuration):
    """A role and its restrictions."""

    name: str
    restrictions: Restrictions

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_role(**data)


def create_role(name: str, *, restrictions: Optional[Restrictions] = None) -> Role:
    """Create a role with the given restrictions.

    Args:
        name: Role name.
        restrictions: Role restrictions.
    """
    if restrictions is None:
        restrictions = dict()
    return Role(name, restrictions)
