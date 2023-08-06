from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

from .._type_utils import PercentileInterpolation, PercentileMode
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class QuantileMeasure(Measure):
    """A quantile measure calculates a given quantile of a vector."""

    _underlying_measures: Sequence[Measure]
    _mode: PercentileMode
    _interpolation: PercentileInterpolation

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measures
        underlying_names = []
        for underlying in self._underlying_measures:
            underlying_names.append(underlying._distil(java_api, cube, None))

        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "CALCULATED_QUANTILE",
            self._mode,
            self._interpolation,
            underlying_names,
        )
        return distilled_name
