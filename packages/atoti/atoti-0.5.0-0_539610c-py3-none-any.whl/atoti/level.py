from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from ._docs_utils import LEVEL_ISIN_DOC, doc
from ._level_conditions import LevelCondition
from ._level_isin_conditions import LevelIsInCondition
from ._repr_utils import ReprJson, convert_repr_json_to_html
from .comparator import Comparator
from .hierarchy import Hierarchy
from .measure import Measure, MeasureConvertible
from .type import DataType


@dataclass
class Level(MeasureConvertible):
    """Level of a Hierarchy."""

    _name: str
    _column_name: str
    _data_type: DataType
    _hierarchy: Optional[Hierarchy] = None
    _comparator: Optional[Comparator] = None

    @property
    def name(self) -> str:
        """Name of the level."""
        return self._name

    @property
    def data_type(self) -> DataType:
        """Type of the level members."""
        return self._data_type

    @property
    def dimension(self) -> str:
        """Name of the dimension holding the level."""
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        return self._hierarchy.dimension

    @property
    def hierarchy(self) -> str:
        """Name of the hierarchy holding the level."""
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        return self._hierarchy.name

    @property
    def _java_description(self) -> str:  # noqa: D401
        """Description for java."""
        return f"{self.name}@{self.hierarchy}@{self.dimension}"

    @property
    def comparator(self) -> Optional[Comparator]:  # noqa: D401
        """Comparator of the level."""
        return self._comparator

    @comparator.setter
    def comparator(self, value: Optional[Comparator]):  # noqa: D401
        """Comparator setter."""
        # pylint: disable=protected-access
        if self._hierarchy is None:
            raise ValueError(f"Missing hierarchy for level {self.name}.")
        self._comparator = value
        self._hierarchy._java_api.update_level_comparator(self)
        self._hierarchy._java_api.refresh_pivot()

    # pylint: disable=unused-argument
    def _to_measure(self, agg_fun: Optional[str] = None) -> Measure:
        """Convert this column into a measure."""
        from ._measures.level_measure import LevelMeasure

        if agg_fun is not None:
            from ._measures.calculated_measure import AggregatedMeasure
            from .scope import LeafLevels

            return AggregatedMeasure(LevelMeasure(self), agg_fun, LeafLevels([self]))
        return LevelMeasure(self)

    @doc(LEVEL_ISIN_DOC)
    def isin(self, *members: Any) -> LevelIsInCondition:
        if None in members:
            raise ValueError("None is not supported in isin conditions.")
        return LevelIsInCondition(self, list(members))

    def __hash__(self) -> int:
        """Return the hash of a tuple describing the Level."""
        return hash(
            (
                self._java_description,  # pylint: disable=protected-access
                self.comparator,
                self._column_name,
            )
        )

    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
            "type": str(self.data_type),
        }
        if self.comparator is not None:
            data[
                "comparator"
            ] = self.comparator._name  # pylint: disable=protected-access
        return (data, {"expanded": True, "root": self.name})

    def _repr_html_(self) -> str:
        return convert_repr_json_to_html(self)

    # Boolean / filtering operations

    def __eq__(self, other: Any) -> LevelCondition:
        """Return an equality condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "eq")

    def __ne__(self, other: Any) -> LevelCondition:
        """Return a non-equality condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "ne")

    def __lt__(self, other: Any) -> LevelCondition:
        """Return a less than condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "lt")

    def __le__(self, other: Any) -> LevelCondition:
        """Return a less or equals condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "le")

    def __gt__(self, other: Any) -> LevelCondition:
        """Return a greater than condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "gt")

    def __ge__(self, other: Any) -> LevelCondition:
        """Return a greater or equal condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "ge")
