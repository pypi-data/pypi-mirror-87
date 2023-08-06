from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..hierarchy import Hierarchy
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..level import Level


@dataclass(eq=False)
class SiblingsAggregationMeasure(Measure):
    """Aggregation measure over a scope."""

    _underlying_measure: Measure
    _agg_fun: str
    _hierarchy: Hierarchy
    _exclude_self: bool = False

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)
        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "SIBLINGS_AGG",
            underlying_name,
            self._hierarchy,
            self._agg_fun,
            self._exclude_self,
        )
        return distilled_name


@dataclass(eq=False)
class WindowAggregationMeasure(Measure):
    """Aggregation measure over a scope."""

    _underlying_measure: Measure
    _agg_fun: str
    _level: Level
    _dense: bool
    _partitioning: Optional[Level]
    _window: Optional[range]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)
        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "WINDOW_AGG",
            underlying_name,
            self._level,
            self._partitioning,
            self._agg_fun,
            (self._window.start, self._window.stop) if self._window else None,
            self._dense,
        )
        return distilled_name
