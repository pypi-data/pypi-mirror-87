from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ._measures.boolean_measure import BooleanMeasure


class Condition(ABC):
    """ABC for conditions which will be used to filter measures."""

    @abstractmethod
    def __and__(self, other: Condition):
        """Override the & bitwise operator to allow users to combine conditions."""

    @abstractmethod
    def _to_measure(self, agg_fun: Optional[str] = None) -> BooleanMeasure:
        """Convert the condition into a measure."""

    def __xor__(self, other: Condition):
        """Throw an exception if the user tries to perform a xor condition."""
        raise Exception("XOR conditions are not supported.")

    def __invert__(self) -> BooleanMeasure:
        """Override the ~ bitwise operator.

        This allows the user to write more complicated conditions when filtering.

        Since Python's built-in ``not`` cannot be overriden to return anything other than a boolean value, the ``~`` bitwise operator is used to reverse the value of a condition.
        """
        from ._measures.boolean_measure import BooleanMeasure

        return BooleanMeasure("invert", [self._to_measure()])

    def __or__(self, other: Condition) -> BooleanMeasure:
        """Override the | bitwise operator to allow users to combine conditions."""
        from ._measures.boolean_measure import BooleanMeasure

        return BooleanMeasure("or", [self._to_measure(), other._to_measure()])
