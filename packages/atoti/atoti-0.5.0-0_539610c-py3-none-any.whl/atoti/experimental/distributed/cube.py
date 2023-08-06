from __future__ import annotations

from typing import TYPE_CHECKING, Collection, Mapping

from ..._local_cube import ALocalCube
from ..._repr_utils import repr_json_cube
from ...aggregates_cache import AggregatesCache
from ...query._cellset import LevelCoordinates
from .hierarchies import DistributedHierarchies
from .levels import DistributedLevels
from .measures import DistributedMeasures

if TYPE_CHECKING:
    from ..._java_api import JavaApi
    from .session import DistributedSession


class DistributedCube(ALocalCube):
    """Cube of a distributed session."""

    def __init__(self, java_api: JavaApi, name: str, session: DistributedSession):
        """Init."""
        super().__init__(
            name,
            java_api,
            session,
            DistributedHierarchies(java_api, self),
            DistributedLevels,
            DistributedMeasures(java_api, self),
            AggregatesCache(java_api, self),
        )

    def _get_level_data_types(
        self, levels_coordinates: Collection[LevelCoordinates]
    ) -> Mapping[LevelCoordinates, str]:
        return {level_coordinates: "object" for level_coordinates in levels_coordinates}

    def _repr_json_(self):
        return repr_json_cube(self)
