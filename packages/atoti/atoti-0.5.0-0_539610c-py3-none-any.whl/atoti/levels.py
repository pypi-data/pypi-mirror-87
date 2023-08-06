from ._base_levels import BaseLevels, _LevelKey
from .hierarchies import Hierarchies
from .level import Level


class Levels(BaseLevels[Level, Hierarchies]):
    """Flat representation of all the levels in the cube."""

    def __delitem__(self, key: _LevelKey):
        """Delete a level.

        Args:
            key: The name of the level to delete, or a ``(hierarchy_name, level_name)`` tuple.
        """
        if key not in self:
            raise KeyError(f"{key} is not an existing level.")
        lvl = self[key]
        hier = lvl._hierarchy
        if hier is None:
            raise ValueError("No hierarchy defined for level " + lvl.name)
        hier._java_api.drop_level(lvl)
        hier._java_api.refresh_pivot()
