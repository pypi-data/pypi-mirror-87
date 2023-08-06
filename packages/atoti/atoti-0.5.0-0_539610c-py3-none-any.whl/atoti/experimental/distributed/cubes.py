from dataclasses import dataclass, field
from typing import Dict, MutableMapping

from ..._java_api import JavaApi
from ..._repr_utils import convert_repr_json_to_html, repr_json_cubes
from .cube import DistributedCube


@dataclass(frozen=True)
class DistributedCubes(MutableMapping[str, DistributedCube]):
    """Manage the distributed cubes."""

    _java_api: JavaApi = field(repr=False)
    _cubes: Dict[str, DistributedCube] = field(default_factory=dict)

    def __getitem__(self, key: str) -> DistributedCube:
        """Get the cube with the given name."""
        return self._cubes[key]

    def __setitem__(self, key: str, value: DistributedCube) -> None:
        """Set the cube for the given name."""
        self._cubes[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete the cube with the given name."""
        try:
            value = self._cubes[key]
            self._java_api.delete_cube(value)
            del self._cubes[key]
            self._java_api.refresh()
        except KeyError:
            raise Exception(f"No cube named {key}") from None

    def __iter__(self):
        """Return the iterator on cubes."""
        return iter(self._cubes)

    def __len__(self) -> int:
        """Return the number of cubes."""
        return len(self._cubes)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_cubes(self)
