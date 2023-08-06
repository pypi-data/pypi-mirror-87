from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Mapping, Tuple

from ._docs_utils import HIERARCHY_ISIN_DOC, doc
from ._hierarchy_isin_conditions import (
    HierarchyIsInCondition,
    create_condition_from_member_paths,
)
from ._repr_utils import convert_repr_json_to_html, repr_json_hierarchy

if TYPE_CHECKING:
    from ._java_api import JavaApi
    from ._local_cube import ALocalCube
    from .level import Level


def _refresh_pivot_decorator(func: Callable) -> Callable:  # type: ignore
    @wraps(func)
    def func_wrapper(self: Hierarchy, *args: Any, **kwArgs: Any) -> Any:
        # pylint: disable=protected-access
        func(self, *args, **kwArgs)
        self._java_api.refresh_pivot()
        # pylint: enable=protected-access

    return func_wrapper


@dataclass
class Hierarchy:
    """Hierarchy of a Cube."""

    _name: str
    _levels: Mapping[str, Level]
    _dimension: str
    _slicing: bool
    _cube: ALocalCube = field(repr=False)
    _java_api: JavaApi = field(repr=False)
    _visible: bool

    @property
    def levels(self) -> Mapping[str, Level]:
        """Levels of the hierarchy."""
        return self._levels

    @property
    def dimension(self) -> str:
        """Name of the dimension of the hierarchy."""
        return self._dimension

    @property
    def slicing(self) -> bool:
        """Whether the hierarchy is slicing or not."""
        return self._slicing

    @property
    def name(self) -> str:
        """Name of the hierarchy."""
        return self._name

    @property
    def visible(self) -> bool:
        """Whether the hierarchy is visible or not."""
        return self._visible

    @property
    def _java_description(self) -> str:  # noqa: D401
        """Description for java."""
        return f"{self.name}@{self.dimension}"

    @levels.setter
    @_refresh_pivot_decorator
    def levels(self, value: Mapping[str, Level]):
        """Levels setter."""
        # pylint: disable=protected-access
        self._levels = value
        self._java_api.create_or_update_hierarchy(
            self._cube, self._dimension, self._name, self._levels
        )
        # pylint: enable=protected-access

    @dimension.setter
    @_refresh_pivot_decorator
    def dimension(self, value: str):
        """Dimension setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_coordinate(self._cube, self, value, self._name)
        self._dimension = value
        # pylint: enable=protected-access

    @slicing.setter
    @_refresh_pivot_decorator
    def slicing(self, value: bool):
        """Slicing setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_slicing(self, value)
        self._slicing = value
        # pylint: enable=protected-access

    @name.setter
    @_refresh_pivot_decorator
    def name(self, value: str):
        """Name setter."""
        # pylint: disable=protected-access
        self._java_api.update_hierarchy_coordinate(
            self._cube, self, self._dimension, value
        )
        self._name = value
        # pylint: enable=protected-access

    @visible.setter
    @_refresh_pivot_decorator
    def visible(self, value: bool):
        """Visibility setter."""
        # pylint: disable=protected-access
        self._java_api.set_hierarchy_visibility(
            self._cube, self._dimension, self._name, value
        )
        self._visible = value
        # pylint: enable=protected-access

    @doc(HIERARCHY_ISIN_DOC)
    def isin(self, *member_paths: Tuple[Any, ...]) -> HierarchyIsInCondition:
        return create_condition_from_member_paths(self, *member_paths)

    def __getitem__(self, key: str) -> Level:
        """Return the level with the given name.

        Args:
            key: The name of the requested level.
        """
        return self.levels[key]

    def _repr_html(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchy(self)

    def __hash__(self) -> int:
        """Return the hash of a tuple describing the Level needed to avoid type error in parent_value."""
        return hash(
            (
                self._java_description,  # pylint: disable=protected-access
                self.slicing,
                self._cube.name,  # pylint: disable=protected-access
            )
        )
