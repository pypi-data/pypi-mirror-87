from __future__ import annotations

from typing import TYPE_CHECKING, Collection

from ..level import Level

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..measure import Measure


def get_measure_name(java_api: JavaApi, measure: Measure, cube: Cube) -> str:
    """Get the name of the measure from either a measure or its name."""
    return measure._distil(java_api, cube, None)


def convert_level_in_description(levels: Collection[Level]) -> Collection[str]:
    """Get descriptions of the passed levels."""
    if any(not isinstance(level, Level) for level in levels):
        raise TypeError("All levels should be of type Level")
    return [lvl._java_description for lvl in levels]  # pylint: disable=protected-access
