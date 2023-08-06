from .._base_levels import BaseLevels
from .hierarchies import QueryHierarchies
from .level import QueryLevel


class QueryLevels(BaseLevels[QueryLevel, QueryHierarchies]):
    """Flat representation of all the levels in the cube."""
