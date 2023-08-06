from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Tuple

from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..level import Level


def parse_time_period(
    time_period: Tuple[Optional[str], Optional[str]]
) -> Tuple[Optional[str], Optional[str]]:
    """Convert the time period into a backward offset and a forward offset."""
    back = time_period[0]
    forward = time_period[1]
    return (
        # Drop the `-` sign.
        back[1:] if back is not None else None,
        forward if forward is not None else None,
    )


@dataclass(eq=False)
class TimePeriodAggregationMeasure(Measure):
    """Aggregation measure over a time period."""

    _underlying_measure: Measure
    _level: Level
    _time_period: Tuple[Optional[str], Optional[str]]
    _agg_fun: str

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measure
        underlying_name = self._underlying_measure._distil(java_api, cube, None)

        back_offset, forward_offset = (
            parse_time_period(self._time_period) if self._time_period else (None, None)
        )

        return java_api.create_measure(
            cube,
            measure_name,
            "TIME_PERIOD_AGGREGATION",
            underlying_name,
            self._level,
            back_offset,
            forward_offset,
            self._agg_fun,
        )
