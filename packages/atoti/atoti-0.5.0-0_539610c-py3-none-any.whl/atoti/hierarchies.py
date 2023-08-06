from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Mapping, Optional, Sequence, Tuple, Union

from ._mappings import DelegateMutableMapping
from ._repr_utils import convert_repr_json_to_html, repr_json_hierarchies
from .hierarchy import Hierarchy
from .level import Level
from .type import NULLABLE_OBJECT

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from .cube import Cube
    from .store import Column


_HierarchyKey = Union[str, Tuple[str, str]]


def _retrieve_hierarchies(
    java_api: JavaApi, cube: Cube
) -> Mapping[Tuple[str, str], Hierarchy]:
    """Retrieve the hierarchies from the cube."""
    return java_api.retrieve_hierarchies(cube)


if TYPE_CHECKING:
    # We import Column in TYPE_CHECKING so no problem here
    LevelOrColumn = Union[Level, Column]  # pylint: disable=used-before-assignment


@dataclass(frozen=True)
class Hierarchies(DelegateMutableMapping[Tuple[str, str], Hierarchy]):
    """Manage the hierarchies."""

    _java_api: JavaApi = field(repr=False)
    _cube: Cube = field(repr=False)

    def _get_underlying(self) -> Mapping[Tuple[str, str], Hierarchy]:
        """Fetch the hierarchies from the JVM each time they are needed."""
        return _retrieve_hierarchies(self._java_api, self._cube)

    def __getitem__(self, key: _HierarchyKey) -> Hierarchy:
        """Return the hierarchy with the given name."""
        (dim, hier) = convert_key(key)
        hierarchies = self._java_api.retrieve_hierarchy(self._cube, dim, hier)
        if len(hierarchies) == 0:
            raise KeyError(f"Unknown hierarchy: {key}")
        if len(hierarchies) == 1:
            return hierarchies[0]
        raise multiple_hierarchies_error(key, hierarchies)

    def __setitem__(
        self,
        key: _HierarchyKey,
        value: Union[Sequence[LevelOrColumn], Mapping[str, LevelOrColumn]],
    ):
        """Add the passed hierarchy or edit the existing one.

        Args:
            key: The name of the hierarchy to add.
            value: The levels of the hierarchy.
                Either a list of levels or store columns, or a mapping from level name to level value or a store column.
        """

        (dim, hier) = convert_key(key)
        if isinstance(value, Sequence):
            value = {column.name: column for column in value}
        elif not isinstance(value, Mapping):
            raise ValueError(
                f"Levels argument is expected to be a sequence or a mapping but is "
                f"{str(type(value).__name__)}"
            )
        # convert to Level
        levels: Mapping[str, Level] = {
            levelName: levelOrColumn
            if isinstance(levelOrColumn, Level)
            else Level(levelName, levelOrColumn.name, NULLABLE_OBJECT)
            for (levelName, levelOrColumn) in value.items()
        }

        # If the hierarchy is a single level hierarchy created from a store field, we
        # automatically put it in a dimension with the same name as the store
        # If the hierarchy is multilevel, the dimension is that of the store of the top most
        # level of the hierarchy.
        if dim is None:
            first_item = (
                value[0] if isinstance(value, Sequence) else list(value.values())[0]
            )
            if isinstance(first_item, Level):
                dim = first_item.dimension
            else:
                dim = first_item._store.name  # pylint: disable=protected-access

        hierarchies = self._java_api.retrieve_hierarchy(self._cube, dim, hier)
        if len(hierarchies) == 1:
            # Edit the existing hierarchy if there is one
            hierarchies[0].levels = levels
        elif len(hierarchies) == 0:
            # Create the new hierarchy
            self._java_api.create_or_update_hierarchy(self._cube, dim, hier, levels)
            self._java_api.refresh_pivot()
        else:
            raise multiple_hierarchies_error(key, hierarchies)

    def __delitem__(self, key: _HierarchyKey):
        """Delete the hierarchy.

        Args:
            key: The name of the hierarchy to delete.
        """
        try:
            self._java_api.drop_hierarchy(self._cube, self[key])
            self._java_api.refresh_pivot()
        except KeyError:
            raise KeyError(f"{key} is not an existing hierarchy.") from None

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchies(self)


def convert_key(key: _HierarchyKey) -> Tuple[Optional[str], str]:
    """Get the dimension and hierarchy from the key."""
    if isinstance(key, str):
        return (None, key)
    if isinstance(key, tuple) and len(key) == 2:
        return key
    raise KeyError(
        "Hierarchy key must be its name or a tuple of two strings (dimension, hierarchy)"
    )


def multiple_hierarchies_error(
    key: _HierarchyKey, hierarchies: Sequence[Hierarchy]
) -> KeyError:
    """Get the error to raise when multiple hierarchies match the key."""
    error_msg = f"Multiple hierarchies with name {key}. "
    error_msg += "Use a tuple to specify the dimension: "
    examples = [
        f'cube.hierarchies[("{hier.dimension}", "{hier.name}")]' for hier in hierarchies
    ]
    error_msg += ", ".join(examples)
    return KeyError(error_msg)
