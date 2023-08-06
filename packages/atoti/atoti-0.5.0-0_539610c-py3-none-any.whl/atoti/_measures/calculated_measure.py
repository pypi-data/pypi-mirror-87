from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence, Union

from .._py4j_utils import as_java_object
from ..measure import Measure
from ..scope._utils import LeafLevels

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube

Operand = Union[Measure, str]


@dataclass(frozen=True)
class Operator:
    """An operator to create a calculated measure from other measures."""

    _name: str
    _operands: Sequence[Operand]

    @staticmethod
    def mul(operands: Sequence[Measure]) -> Operator:
        """Multiplication operator."""
        return Operator("mul", operands)

    @staticmethod
    def truediv(operands: Sequence[Measure]) -> Operator:
        """Division operator."""
        return Operator("truediv", operands)

    @staticmethod
    def floordiv(operands: Sequence[Measure]) -> Operator:
        """Division operator."""
        return Operator("floordiv", operands)

    @staticmethod
    def add(operands: Sequence[Measure]) -> Operator:
        """Addition operator."""
        return Operator("add", operands)

    @staticmethod
    def sub(operands: Sequence[Measure]) -> Operator:
        """Subtraction operator."""
        return Operator("sub", operands)

    @staticmethod
    def neg(operand: Measure) -> Operator:
        """Neg operator."""
        return Operator("neg", [operand])

    @staticmethod
    def mod(operands: Sequence[Measure]) -> Operator:
        """Modulo operator."""
        return Operator("mod", operands)


@dataclass(eq=False)
class CalculatedMeasure(Measure):
    """A calculated measure is the result of an operation between other measures."""

    _operator: Operator

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        # Distil the underlying measures
        underlying_names = []
        for operand in self._operator._operands:  # pylint: disable=protected-access
            if isinstance(operand, Measure):
                u_name = operand._distil(java_api, cube, None)
            else:
                u_name = as_java_object(java_api.gateway, operand)

            underlying_names.append(u_name)

        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "CALCULATED",
            self._operator._name,  # pylint: disable=protected-access
            underlying_names,
        )
        return distilled_name


@dataclass(eq=False)
class AggregatedMeasure(Measure):
    """Aggregated Measure."""

    _underlying_measure: Measure
    _agg_fun: str
    _on_levels: Optional[LeafLevels]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        underlying_name = self._underlying_measure._distil(  # pylint: disable=protected-access
            java_api, cube, None
        )

        distilled_name = java_api.create_measure(
            cube,
            measure_name,
            "LEAF_AGGREGATION",
            underlying_name,
            self._on_levels.levels if self._on_levels else [],
            self._agg_fun,
        )
        return distilled_name
