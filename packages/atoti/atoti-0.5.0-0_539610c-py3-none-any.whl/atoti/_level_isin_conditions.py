from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Collection, Optional, Union

from ._condition import Condition
from .measure import MeasureConvertible

if TYPE_CHECKING:
    from ._measures.boolean_measure import BooleanMeasure
    from ._multi_condition import MultiCondition
    from .level import Level
    from .query.level import QueryLevel


@dataclass(frozen=True)
class LevelIsInCondition(Condition, MeasureConvertible):
    """Class for isin condition on cube levels."""

    _level: Union[Level, QueryLevel]
    _members: Collection[Any]
    _operation: str = "li"

    def __and__(self, other: Condition) -> MultiCondition:
        """Override the ``&`` bitwise operator to allow users to combine conditions."""
        from ._level_conditions import LevelCondition
        from ._measures.boolean_measure import BooleanMeasure
        from ._multi_condition import MultiCondition

        if isinstance(other, BooleanMeasure):
            return MultiCondition(
                _level_isin_conditions=(self,), _measure_conditions=(other,)
            )

        if isinstance(other, LevelCondition):
            return MultiCondition(
                _level_isin_conditions=(self,), _level_conditions=(other,)
            )

        if isinstance(other, LevelIsInCondition):
            return MultiCondition(_level_isin_conditions=(self, other))

        if isinstance(other, MultiCondition):
            return MultiCondition(
                other._level_conditions,
                other._measure_conditions,
                tuple(other._level_isin_conditions) + (self,),
                other._hierarchy_isin_condition,
            )

        raise ValueError("Invalid condition provided.")

    # pylint: disable=unused-argument
    def _to_measure(self, agg_fun: Optional[str] = None) -> BooleanMeasure:
        """Convert this object into a boolean measure.

        Args:
            agg_fun: The aggregation function.

        """
        from ._measures.boolean_measure import BooleanMeasure
        from .query.level import QueryLevel

        if isinstance(self._level, QueryLevel):
            raise ValueError("Query level conditions cannot be converted to measures")

        if len(self._members) == 1:
            return (self._level == list(self._members)[0])._to_measure()

        return BooleanMeasure(
            "or", [(self._level == value)._to_measure() for value in self._members]
        )
