from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

import pandas as pd

from ._docs_utils import doc
from ._hierarchy_isin_conditions import HierarchyIsInCondition
from ._java_api import JavaApi
from ._level_conditions import LevelCondition
from ._level_isin_conditions import LevelIsInCondition
from ._local_session import ALocalSession
from ._multi_condition import MultiCondition
from ._query_plan import QueryAnalysis
from ._repr_utils import convert_repr_json_to_html
from ._type_utils import BASE_SCENARIO, ScenarioName, typecheck
from .aggregates_cache import AggregatesCache
from .experimental.distributed.hierarchies import DistributedHierarchies
from .experimental.distributed.levels import DistributedLevels
from .experimental.distributed.measures import DistributedMeasures
from .hierarchies import Hierarchies
from .level import Level
from .levels import Levels
from .measures import Measures
from .named_measure import NamedMeasure
from .query._cellset import LevelCoordinates
from .query.cube import _QUERY_ARGS_DOC, _QUERY_DOC
from .query.level import QueryLevel
from .query.measure import QueryMeasure
from .query.query_result import QueryResult

if TYPE_CHECKING:

    from ._repr_utils import ReprJson

_Hierarchies = TypeVar("_Hierarchies", Hierarchies, DistributedHierarchies)
_Level = TypeVar("_Level", Level, QueryLevel)
_Levels = TypeVar("_Levels", Levels, DistributedLevels)
_Measure = TypeVar("_Measure", NamedMeasure, QueryMeasure)
_Measures = TypeVar("_Measures", Measures, DistributedMeasures)

BucketRows = Union[Dict[Tuple[Any, ...], Dict[str, Any]], pd.DataFrame, List[List[Any]]]


@typecheck
class ALocalCube(ABC):
    """Abstract cube class."""

    def __init__(
        self,
        name: str,
        java_api: JavaApi,
        session: ALocalSession,
        hierarchies: _Hierarchies,
        level_function: Callable[[_Hierarchies], _Levels],
        measures: _Measures,
        agg_cache: AggregatesCache,
    ):
        """Init."""
        self._name = name
        self._java_api = java_api
        self._session = session
        self._hierarchies = hierarchies
        self._levels = level_function(self._hierarchies)
        self._measures = measures
        self._agg_cache = agg_cache

    @property
    def name(self) -> str:
        """Name of the cube."""
        return self._name

    @property
    def hierarchies(self) -> _Hierarchies:
        """Hierarchies of the cube."""
        return self._hierarchies

    @property
    def levels(self) -> _Levels:
        """Levels of the cube."""
        return self._levels

    @property
    def measures(self) -> _Measures:
        """Measures of the cube."""
        return self._measures

    @property
    def aggregates_cache(self) -> AggregatesCache:  # noqa: D401
        """Aggregates cache of the cube."""
        return self._agg_cache

    @abstractmethod
    def _get_level_data_types(
        self, levels_coordinates: Collection[LevelCoordinates]
    ) -> Mapping[LevelCoordinates, str]:
        ...

    @doc(_QUERY_DOC)
    def query(
        self,
        *measures: _Measure,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> QueryResult:
        mdx = self._generate_mdx(
            measures, ScenarioName(scenario), levels=levels, condition=condition
        )
        return self._session.query_mdx(mdx, timeout=timeout)

    @doc(args=_QUERY_ARGS_DOC)
    def explain_query(
        self,
        *measures: _Measure,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
        scenario: str = BASE_SCENARIO,
        timeout: int = 30,
    ) -> QueryAnalysis:
        """Run the query but return an explanation of the query instead of the result.

        The explanation contains a summary, global timings and the query plan with all the retrievals.

        {args}

        Returns:
            The query explanation.
        """
        mdx = self._generate_mdx(
            measures, ScenarioName(scenario), levels=levels, condition=condition
        )
        return self._java_api.analyse_mdx(mdx, timeout)

    def _generate_mdx(
        self,
        measures: Sequence[_Measure],
        scenario: ScenarioName,
        *,
        levels: Optional[Union[_Level, Sequence[_Level]]] = None,
        condition: Optional[
            Union[
                LevelCondition,
                MultiCondition,
                LevelIsInCondition,
                HierarchyIsInCondition,
            ]
        ] = None,
    ) -> str:
        query_measures = [
            QueryMeasure(
                measure.name,
                measure.visible,
                measure.folder,
                measure.formatter,
                measure.description,
            )
            for measure in measures
        ]
        query_levels = (
            [
                QueryLevel(level.name, level.dimension, level.hierarchy)
                for level in (levels or [])
            ]
            if isinstance(levels, Sequence) or levels is None
            else [QueryLevel(levels.name, levels.dimension, levels.hierarchy)]
        )
        return (
            self._session._open_transient_query_session()  # pylint: disable=protected-access
            .cubes[self.name]
            ._generate_mdx(query_measures, query_levels, scenario, condition=condition)
        )

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    @abstractmethod
    def _repr_json_(self) -> ReprJson:
        ...
