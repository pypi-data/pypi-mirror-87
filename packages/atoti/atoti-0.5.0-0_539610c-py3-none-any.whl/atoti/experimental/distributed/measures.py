from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict

from atoti.query.measure import QueryMeasure

from ..._mappings import DelegateMutableMapping
from ..._repr_utils import convert_repr_json_to_html, repr_json_measures
from ...exceptions import AtotiJavaException
from ...measure import MeasureLike

if TYPE_CHECKING:
    from ..._java_api import JavaApi
    from .cube import DistributedCube


@dataclass(frozen=True)
class DistributedMeasures(DelegateMutableMapping[str, QueryMeasure]):
    """Manage the measures."""

    _java_api: JavaApi = field(repr=False)
    _cube: DistributedCube = field(repr=False)

    def _get_underlying(self) -> Dict[str, QueryMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        cube_measures = self._java_api.get_full_measures(self._cube)
        return {
            name: QueryMeasure(
                name,
                cube_measures[name].visible,
                cube_measures[name].folder,
                cube_measures[name].formatter,
                cube_measures[name].description,
            )
            for name in cube_measures
        }

    def __getitem__(self, key: str) -> QueryMeasure:
        """Return the measure with the given name."""
        try:
            cube_measure = self._java_api.get_measure(self._cube, key)
            return QueryMeasure(
                key,
                cube_measure.visible,
                cube_measure.folder,
                cube_measure.formatter,
                cube_measure.description,
            )
        except AtotiJavaException:
            raise KeyError(f"No measure named {key}") from None

    def __setitem__(self, key: str, value: MeasureLike):
        """Publish the measure with the given name.

        If the input is not a Measure, its ``_to_measure`` method will be called.

        Args:
            key: The name of the measure to add.
            value: The measure to add.
        """
        raise AttributeError("Distributed cube measures cannot be changed")

    def __delitem__(self, key: str):
        """Delete a measure.

        Args:
            key: The name of the measure to delete.
        """
        raise AttributeError("Distributed cube measures cannot be changed")

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_measures(self)
