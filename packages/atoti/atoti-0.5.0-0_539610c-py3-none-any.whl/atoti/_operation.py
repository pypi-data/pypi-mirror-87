from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ._measures.literal_measure import LiteralMeasure
from ._measures.store_measure import StoreMeasure
from .measure import Measure, MeasureConvertible

if TYPE_CHECKING:
    from .store import Column


def _to_operation(obj: Any) -> Operation:
    """Convert an object to an operation if is not already one.

    Args:
        obj: the object to convert.

    Returns:
        The operation corresponding to the given object.
    """
    if isinstance(obj, Operation):
        return obj

    if isinstance(obj, Measure):
        raise TypeError("Measures cannot be converted to an operation")

    from .store import Column  # pylint: disable=redefined-outer-name

    if isinstance(obj, Column):
        return ColumnOperation(obj)

    return ConstantOperation(obj)


@dataclass(frozen=True)
class Operation(MeasureConvertible, ABC):
    """An Operation between scalar and store columns."""

    @abstractmethod
    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        """Convert the operation to a measure."""

    def __mul__(self, other: Any):
        """Override the * operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return MultiplicationOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other: Any):
        """Override the * operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return MultiplicationOperation(other_op, self)
        except TypeError:
            return NotImplemented

    def __truediv__(self, other: Any):
        """Override the / operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return DivisionOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, other: Any):
        """Override the / operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return DivisionOperation(other_op, self)
        except TypeError:
            return NotImplemented

    def __add__(self, other: Any):
        """Override the + operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return AdditionOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __radd__(self, other: Any):
        """Override the + operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return AdditionOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __sub__(self, other: Any):
        """Override the - operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return SubtractionOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __rsub__(self, other: Any):
        """Override the - operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return SubtractionOperation(other_op, self)
        except TypeError:
            return NotImplemented

    def __eq__(self, other: Any):
        """Override the == operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return EqualOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __ne__(self, other: Any):
        """Override the != operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return NotEqualOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __lt__(self, other: Any):
        """Override the < operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return LowerThanOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __gt__(self, other: Any):
        """Override the > operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return GreaterThanOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __le__(self, other: Any):
        """Override the <= operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return LowerThanOrEqualOperation(self, other_op)
        except TypeError:
            return NotImplemented

    def __ge__(self, other: Any):
        """Override the >= operator to delay the conversion."""
        try:
            other_op: Operation = _to_operation(other)
            return GreaterThanOrEqualOperation(self, other_op)
        except TypeError:
            return NotImplemented


@dataclass(frozen=True)
class ColumnOperation(Operation):
    """Column of a store in an operation."""

    _column: Column

    def _to_measure(self, agg_fun: Optional[str] = None) -> StoreMeasure:
        return StoreMeasure(
            self._column,
            agg_fun,
            self._column._store,  # pylint: disable=protected-access
        )


@dataclass(frozen=True)
class ConstantOperation(Operation):
    """Constant leaf of an operation."""

    _value: Any

    def _to_measure(
        self, agg_fun: Optional[str] = None
    ) -> Measure:  # pylint: disable=unused-argument
        return LiteralMeasure(self._value)


@dataclass(frozen=True)
class MultiplicationOperation(Operation):
    """Multiplication operation."""

    _multiplier: Operation
    _multiplicand: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        multiplier = self._multiplier._to_measure(agg_fun)
        multiplicand = self._multiplicand._to_measure(agg_fun)
        _throw_fact_level_operation(multiplier, multiplicand)
        return multiplier * multiplicand


@dataclass(frozen=True)
class AdditionOperation(Operation):
    """Addition operation."""

    _augend: Operation
    _addend: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        augend = self._augend._to_measure(agg_fun)
        addend = self._addend._to_measure(agg_fun)
        _throw_fact_level_operation(augend, addend)
        return augend + addend


@dataclass(frozen=True)
class SubtractionOperation(Operation):
    """Subtraction operation."""

    _minuend: Operation
    _subtrahend: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        minuend = self._minuend._to_measure(agg_fun)
        subtrahend = self._subtrahend._to_measure(agg_fun)
        _throw_fact_level_operation(minuend, subtrahend)
        return minuend - subtrahend


@dataclass(frozen=True)
class DivisionOperation(Operation):
    """Division operation."""

    _dividend: Operation
    _divisor: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        dividend = self._dividend._to_measure(agg_fun)
        divisor = self._divisor._to_measure(agg_fun)
        _throw_fact_level_operation(dividend, divisor)
        return dividend / divisor


@dataclass(frozen=True)
class EqualOperation(Operation):
    """== operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        _throw_fact_level_operation(left, right)
        return left == right


@dataclass(frozen=True)
class NotEqualOperation(Operation):
    """!= operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        return left != right


@dataclass(frozen=True)
class GreaterThanOperation(Operation):
    """> operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        return left > right


@dataclass(frozen=True)
class GreaterThanOrEqualOperation(Operation):
    """>= operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        return left >= right


@dataclass(frozen=True)
class LowerThanOperation(Operation):
    """< operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        return left < right


@dataclass(frozen=True)
class LowerThanOrEqualOperation(Operation):
    """<= operation."""

    _left: Operation
    _right: Operation

    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        left = self._left._to_measure(agg_fun)
        right = self._right._to_measure(agg_fun)
        return left <= right


def _throw_fact_level_operation(column1: Measure, column2: Measure):
    """Raise an error because fact level operations are not supported in measures.

    Args:
        column1: the first column of the operation
        column2: the second column of the operation

    """
    if (isinstance(column1, StoreMeasure) and isinstance(column2, LiteralMeasure)) or (
        isinstance(column1, LiteralMeasure) and isinstance(column2, StoreMeasure)
    ):
        raise NotImplementedError(
            "It is not possible to create a measure by combining a store column"
            " and a constant. You can create a new store column instead."
        )
    if isinstance(column1, StoreMeasure) and isinstance(column2, StoreMeasure):
        raise NotImplementedError(
            "It is not possible to create a measure by combining 2 store columns."
            " You can create a new store column instead."
        )
