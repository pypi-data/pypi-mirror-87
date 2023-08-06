from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Set

from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..level import Level


@dataclass(eq=False)
class RestrictedMeasure(Measure):
    """A measure that has no values unless some required levels are expressed in the query."""

    _underlying: Measure
    _required_levels: Set[Level]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = self._underlying._distil(java_api, cube, None)

        distilled_name = java_api.create_measure(
            cube, measure_name, "LEAF_NOAGG", underlying_name, self._required_levels
        )

        return distilled_name
