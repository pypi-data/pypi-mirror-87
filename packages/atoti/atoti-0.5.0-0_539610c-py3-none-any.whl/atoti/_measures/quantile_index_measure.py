from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

from .._type_utils import PercentileIndexInterpolation, PercentileMode
from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube


@dataclass(eq=False)
class QuantileIndexMeasure(Measure):
    """A quantile index measure calculates the index of a given quantile in a vector."""

    _underlying_measures: Sequence[Measure]
    _mode: PercentileMode
    _interpolation: PercentileIndexInterpolation

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distill the underlying measures
        underlying_names = []
        for underlying in self._underlying_measures:
            underlying_names.append(underlying._distil(java_api, cube, None))

        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "CALCULATED_QUANTILE_INDEX",
            self._mode,
            self._interpolation,
            underlying_names,
        )
        return distilled_name
