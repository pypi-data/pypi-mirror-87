from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping, Optional, Sequence, Tuple, Union

from ..._mappings import DelegateMutableMapping, ImmutableMapping
from ..._repr_utils import convert_repr_json_to_html, repr_json_hierarchies
from ...hierarchies import convert_key, multiple_hierarchies_error
from ...hierarchy import Hierarchy
from ...level import Level
from ...query.hierarchy import QueryHierarchy
from ...query.level import QueryLevel

if TYPE_CHECKING:
    from ..._java_api import JavaApi
    from ...store import Column
    from .cube import DistributedCube

    LevelOrColumn = Union[Level, Column]


_HierarchyKey = Union[str, Tuple[str, str]]


def _cube_hierarchy_to_query_hierarchy(hierarchy: Hierarchy) -> QueryHierarchy:
    """Convert a cube hierarchy into a query hierarchy."""
    return QueryHierarchy(
        hierarchy.name,
        hierarchy.dimension,
        to_query_levels(hierarchy.levels),
        hierarchy.slicing,
    )


def _retrieve_hierarchies(
    java_api: JavaApi, cube: DistributedCube
) -> Mapping[Tuple[str, str], QueryHierarchy]:
    """Retrieve the hierarchies from the cube."""
    hierarchies = java_api.retrieve_hierarchies(cube)
    return {
        hierarchyCoordinate: _cube_hierarchy_to_query_hierarchy(
            hierarchies[hierarchyCoordinate]
        )
        for hierarchyCoordinate in hierarchies
    }


def _cube_level_to_query_level(level: Level) -> QueryLevel:
    """Convert a cube level into a query level."""
    return QueryLevel(level.name, level.dimension, level.hierarchy)


def to_query_levels(levels: Mapping[str, Level]) -> ImmutableMapping[str, QueryLevel]:
    """Convert a dict of cube levels into a dict of query levels."""
    return ImmutableMapping(
        {
            levelName: _cube_level_to_query_level(levels[levelName])
            for levelName in levels
            if levelName != "ALL"
        }
    )


@dataclass(frozen=True)
class DistributedHierarchies(DelegateMutableMapping[Tuple[str, str], QueryHierarchy]):
    """Manage the hierarchies."""

    _java_api: JavaApi = field(repr=False)
    _cube: DistributedCube = field(repr=False)

    def _get_underlying(self) -> Mapping[Tuple[str, str], QueryHierarchy]:
        """Fetch the hierarchies from the JVM each time they are needed."""
        return _retrieve_hierarchies(self._java_api, self._cube)

    @staticmethod
    def _convert_key(key: _HierarchyKey) -> Tuple[Optional[str], str]:
        """Get the dimension and hierarchy from the key."""
        if isinstance(key, str):
            return None, key
        if isinstance(key, tuple) and len(key) == 2:
            return key
        raise KeyError(
            "Hierarchy key must be its name or a tuple of two strings (dimension, hierarchy)"
        )

    def __getitem__(self, key: _HierarchyKey) -> QueryHierarchy:
        """Return the hierarchy with the given name."""
        (dim, hier) = convert_key(key)
        cube_hierarchies = self._java_api.retrieve_hierarchy(self._cube, dim, hier)
        hierarchies = [_cube_hierarchy_to_query_hierarchy(h) for h in cube_hierarchies]
        if len(hierarchies) == 0:
            raise KeyError(f"Unknown hierarchy: {key}")
        if len(hierarchies) == 1:
            return hierarchies[0]
        raise multiple_hierarchies_error(key, cube_hierarchies)

    def __setitem__(
        self,
        key: _HierarchyKey,
        value: Union[Sequence[LevelOrColumn], Mapping[str, LevelOrColumn]],
    ):
        """Add the passed hierarchy or edit the existing one.

        Args:
            key: The name of the hierarchy to add.
            value: The levels of the hierarchy.
                Either a list of levels or store columns, or a mapping from level name to level
                value or a store column.
        """
        raise AttributeError("Distributed cube hierarchies cannot be changed")

    def __delitem__(self, key: _HierarchyKey):
        """Delete the hierarchy.

        Args:
            key: The name of the hierarchy to delete.
        """
        raise AttributeError("Distributed cube hierarchies cannot be changed")

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchies(self)
