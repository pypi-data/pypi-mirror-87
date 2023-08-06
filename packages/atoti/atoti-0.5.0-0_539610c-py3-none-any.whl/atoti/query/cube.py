from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, List, Optional, Sequence, Union

from .._docs_utils import doc
from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._multi_condition import MultiCondition
from .._repr_utils import convert_repr_json_to_html, repr_json_cube
from .._type_utils import BASE_SCENARIO, ScenarioName
from ._mdx_utils import generate_mdx
from .hierarchies import QueryHierarchies
from .level import QueryLevel
from .levels import QueryLevels
from .measure import QueryMeasure
from .measures import QueryMeasures
from .query_result import QueryResult

if TYPE_CHECKING:
    from .session import QuerySession

_QUERY_ARGS_DOC = """Args:
            measures: The measures to query.
                If ``None``, all the measures are queried.
            levels: The levels to split on.
                If ``None``, the value of the measures at the top of the cube is returned.
            condition: The filtering condition.
                Only conditions on level equality with a string are supported.
                For instance:

                * ``lvl["Country"] == "France"``
                * ``(lvl["Country"] == "USA") & (lvl["Currency"] == "USD")``

            scenario: The scenario to query.
            timeout: The query timeout in seconds.
"""

_QUERY_DOC = f"""Query the cube to get the value of some measures.

        The value of the measures is given on all the members of the given levels.

        {_QUERY_ARGS_DOC}

        Returns:
            The resulting DataFrame.
"""


@dataclass(frozen=True)
class QueryCube:
    """Query cube."""

    name: str
    """Name of the cube."""

    hierarchies: QueryHierarchies
    """Hierarchies of the cube."""

    measures: QueryMeasures
    """Measures of the cube."""

    _session: QuerySession = field(repr=False)

    @property
    def levels(self) -> QueryLevels:
        """Levels of the cube."""
        return QueryLevels(self.hierarchies)

    def _generate_mdx(
        self,
        measures: Sequence[QueryMeasure],
        levels: Sequence[QueryLevel],
        scenario: ScenarioName,
        *,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
    ) -> str:
        conditions: List[LevelCondition] = []
        level_isin_condition: List[LevelIsInCondition] = []
        hierarchy_isin_condition: List[HierarchyIsInCondition] = []
        if condition:
            if isinstance(condition, LevelCondition):
                conditions.append(condition)
            elif isinstance(condition, LevelIsInCondition):
                level_isin_condition.append(condition)
            elif isinstance(condition, HierarchyIsInCondition):
                hierarchy_isin_condition.append(condition)
            elif isinstance(condition, MultiCondition):
                measure_conditions = (
                    condition._measure_conditions  # pylint: disable=protected-access
                )
                if measure_conditions:
                    raise ValueError(
                        f"Multi-conditions with measures are not supported when querying cube:"
                        f" {measure_conditions}"
                    )
                conditions.extend(
                    condition._level_conditions  # pylint: disable=protected-access
                )
                level_isin_condition.extend(
                    condition._level_isin_conditions  # pylint: disable=protected-access
                )
                hierarchy_isin_condition.extend(
                    condition._hierarchy_isin_condition  # pylint: disable=protected-access
                )
            else:
                raise TypeError(
                    f"Unexpected type of query condition: f{type(condition)}"
                )
        return generate_mdx(
            self,
            measures,
            levels,
            scenario,
            conditions,
            level_isin_condition,
            hierarchy_isin_condition,
        )

    @doc(_QUERY_DOC)
    def query(
        self,
        *measures: QueryMeasure,
        levels: Optional[Union[QueryLevel, Sequence[QueryLevel]]] = None,
        condition: Optional[Union[LevelCondition, MultiCondition]] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
        **kwargs: Any,
    ) -> QueryResult:
        levels = [levels] if isinstance(levels, QueryLevel) else (levels or [])
        mdx = self._generate_mdx(
            measures, levels, ScenarioName(scenario), condition=condition
        )
        return self._session.query_mdx(mdx, timeout=timeout, **kwargs)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_cube(self)
