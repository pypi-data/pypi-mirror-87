from abc import abstractmethod
from dataclasses import dataclass
from typing import Collection, Optional, Tuple

from atoti._measures.scope_aggregation_measure import (
    SiblingsAggregationMeasure,
    WindowAggregationMeasure,
)
from atoti._measures.time_period_measure import TimePeriodAggregationMeasure
from atoti.hierarchy import Hierarchy
from atoti.level import Level
from atoti.measure import Measure

from .scope import Scope


@dataclass(frozen=True)
class Window(Scope):
    """Window-like structure used in the computation of cumulative aggregations."""

    @abstractmethod
    def _create_aggregated_measure(self, measure: Measure, agg_fun: str) -> Measure:
        """Create the appropriate aggregated measure for this window.

        Args:
            measure: The underlying measure to aggregate
            agg_fun: The aggregation function to use.
        """


@dataclass(frozen=True)
class CumulativeWindow(Window):
    """Implementation of a Window for member-based cumulative aggregations.

    It contains a level, its range of members which is (-inf, 0) by default, and a partitioning consisting of levels in that hierarchy.
    """

    _level: Level
    _dense: bool
    _window: Optional[range]
    _partitioning: Optional[Level] = None

    def _create_aggregated_measure(self, measure: Measure, agg_fun: str) -> Measure:
        return WindowAggregationMeasure(
            measure,
            agg_fun,
            self._level,
            self._dense,
            self._partitioning,
            self._window,
        )


@dataclass(frozen=True)
class CumulativeTimeWindow(Window):
    """Implementation of a Window for time-based cumulative aggregations.

    It contains a level, its time range defined by two strings, and a partitioning consisting of levels in that hierarchy.
    """

    _level: Level
    _window: Tuple[Optional[str], Optional[str]]
    _partitioning: Optional[Level] = None

    def _create_aggregated_measure(self, measure: Measure, agg_fun: str) -> Measure:
        return TimePeriodAggregationMeasure(measure, self._level, self._window, agg_fun)


@dataclass(frozen=True)
class SiblingsWindow(Window):
    """Implementation of a Window for sibling aggregations.

    It contains at least hierarchy, and whether to exclude the current member from the calculations (useful when computing marginal aggregations).
    """

    _hierarchy: Hierarchy
    _exclude_self: bool = False

    def _create_aggregated_measure(self, measure: Measure, agg_fun: str) -> Measure:
        return SiblingsAggregationMeasure(
            measure, agg_fun, self._hierarchy, self._exclude_self
        )


@dataclass(frozen=True)
class LeafLevels(Scope):
    """A collection of levels or level names, used in dynamic aggregation operations."""

    _levels: Collection[Level]

    @property
    def levels(self):
        """Dynamic aggregation levels."""
        return self._levels
