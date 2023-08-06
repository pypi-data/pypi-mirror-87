from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Collection, Optional

from ..measure import Measure

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..cube import Cube
    from ..level import Level
    from ..scope import LeafLevels
    from ..store import Column, Store


@dataclass(eq=False)
class StoreMeasure(Measure):
    """Measure based on the column of a store."""

    _column: Column
    _agg_fun: Optional[str]
    _store: Store = field(repr=False)

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        agg_fun = self._agg_fun or "SINGLE_VALUE_NULLABLE"
        levels = (
            []
            if agg_fun != "SINGLE_VALUE_NULLABLE"
            else [cube.levels[column] for column in self._store.keys]
        )
        distilled_name = java_api.aggregated_measure(
            cube, measure_name, self._store.name, self._column.name, agg_fun, levels
        )
        return distilled_name


@dataclass(eq=False)
class SingleValueStoreMeasure(Measure):
    """Single value aggregated measure based on the column of a store."""

    _column: Column
    _levels: Optional[Collection[Level]]

    def _do_distil(
        self, java_api: JavaApi, cube: Cube, measure_name: Optional[str] = None
    ) -> str:
        store = self._column._store  # pylint: disable=protected-access
        levels = (
            [cube.levels[column] for column in store.keys]
            if self._levels is None
            else self._levels
        )

        distilled_name = java_api.aggregated_measure(
            cube,
            measure_name,
            store.name,
            self._column.name,
            "SINGLE_VALUE_NULLABLE",
            levels,
        )

        return distilled_name
