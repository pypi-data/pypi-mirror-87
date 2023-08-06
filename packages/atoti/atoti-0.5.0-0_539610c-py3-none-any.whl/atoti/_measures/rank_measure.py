from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..hierarchy import Hierarchy
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class RankMeasure(Measure):
    """Ranking of hierarchy members based on their values for a measure."""

    _underlying_measure: Measure
    _hierarchy: Hierarchy
    _ascending: bool
    _apply_filters: bool

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        u_name = self._underlying_measure._distil(java_api, cube, None)

        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "RANK",
            u_name,
            self._hierarchy,
            self._ascending,
            self._apply_filters,
        )
        return distilled_name
