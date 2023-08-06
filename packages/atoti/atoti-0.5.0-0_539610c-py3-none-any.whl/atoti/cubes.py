from dataclasses import dataclass, field
from typing import Dict, MutableMapping

from ._ipython_utils import ipython_key_completions_for_mapping
from ._java_api import JavaApi
from ._repr_utils import convert_repr_json_to_html, repr_json_cubes
from .cube import Cube


@dataclass(frozen=True)
class Cubes(MutableMapping[str, Cube]):
    """Manage the cubes of the session."""

    _java_api: JavaApi = field(repr=False)
    _cubes: Dict[str, Cube] = field(default_factory=dict)

    def __getitem__(self, key: str) -> Cube:
        """Get the cube with the given name."""
        return self._cubes[key]

    def __setitem__(self, key: str, value: Cube) -> None:
        """Set the cube for the given name."""
        self._cubes[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete the cube with the given name."""
        try:
            value = self._cubes[key]
            self._java_api.delete_cube(value)
            del self._cubes[key]
            self._java_api.refresh_pivot()
        except KeyError:
            raise Exception(f"No cube named {key}") from None

    def __iter__(self):
        """Return the iterator on cubes."""
        return iter(self._cubes)

    def __len__(self) -> int:
        """Return the number of cubes."""
        return len(self._cubes)

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_cubes(self)
