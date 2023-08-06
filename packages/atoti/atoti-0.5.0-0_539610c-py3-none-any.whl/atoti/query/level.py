from dataclasses import dataclass
from typing import Any

from .._docs_utils import LEVEL_ISIN_DOC, doc
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._repr_utils import ReprJson, convert_repr_json_to_html
from ..measure import Measure


@dataclass(frozen=True)
class QueryLevel:
    """Level of a query cube."""

    name: str
    """Name of the level."""

    dimension: str
    """Dimension of the level."""

    hierarchy: str
    """Hierarchy of the level."""

    @doc(LEVEL_ISIN_DOC)
    def isin(self, *members: Any) -> LevelIsInCondition:
        if None in members:
            raise ValueError("None is not supported in isin conditions.")
        return LevelIsInCondition(self, list(members))

    def __eq__(self, other: Any) -> LevelCondition:
        """Return an equality condition against this level."""
        if isinstance(other, Measure):
            return NotImplemented
        return LevelCondition(self, other, "eq")

    def __ne__(self, other: Any) -> LevelCondition:
        """Not supported."""
        # Explicitly implemented so that Python doesn't just silently return False.
        raise NotImplementedError(
            "Query level conditions can only be based on equality (==)."
        )

    @property
    def _java_description(self) -> str:  # noqa: D401
        """Description for Java."""
        return f"{self.name}@{self.hierarchy}@{self.dimension}"

    def _repr_json_(self) -> ReprJson:
        data = {
            "dimension": self.dimension,
            "hierarchy": self.hierarchy,
        }
        return (
            data,
            {"expanded": True, "root": self.name},
        )

    def _repr_html_(self) -> str:
        return convert_repr_json_to_html(self)
