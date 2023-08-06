from ..._base_levels import BaseLevels
from ...query.level import QueryLevel
from .hierarchies import DistributedHierarchies


class DistributedLevels(BaseLevels[QueryLevel, DistributedHierarchies]):
    """Flat representation of all the levels in the cube."""
