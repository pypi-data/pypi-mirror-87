import operator
from dataclasses import dataclass, field
from itertools import chain
from typing import (
    Dict,
    Generic,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from ._ipython_utils import ipython_key_completions_for_mapping
from ._repr_utils import ReprJson, convert_repr_json_to_html
from .experimental.distributed.hierarchies import DistributedHierarchies
from .hierarchies import Hierarchies
from .hierarchy import Hierarchy
from .level import Level
from .query.hierarchies import QueryHierarchies
from .query.level import QueryLevel

_Level = TypeVar("_Level", Level, QueryLevel)
_Hierarchies = TypeVar(
    "_Hierarchies", Hierarchies, QueryHierarchies, DistributedHierarchies
)

_LevelKey = Union[str, Tuple[str, str], Tuple[str, str, str]]


@dataclass(frozen=True)
class BaseLevels(Generic[_Level, _Hierarchies], Mapping[_LevelKey, _Level]):  # type: ignore
    """Base class to manipulate flattened levels."""

    _hierarchies: _Hierarchies = field(repr=False)

    @staticmethod
    def _raise_mutliplelevel_error(level_name: str, hierarchies: List[Hierarchy]):
        error_msg = f"Multiple levels named {level_name}. "
        error_msg += (
            "Use a tuple to specify the hierarchy and the dimension if necessary: "
        )
        examples = [
            f'cube.levels[("{hierarchy.dimension}", "{hierarchy.name}", "{level_name}")]'
            for hierarchy in hierarchies
        ]
        error_msg += ", ".join(examples)
        raise KeyError(error_msg)

    def _flatten(self) -> Mapping[str, Optional[_Level]]:
        flat_levels: Dict[str, Optional[_Level]] = dict()
        for hierarchy in self._hierarchies.values():
            for level in hierarchy.levels.values():
                if level.name in flat_levels:
                    # None is used as a flag to mark levels appearing in multiple hiearchies.
                    # When it happens, the user must use a tuple to retrieve the level.
                    # Like that: (hierarchy name, level name).
                    flat_levels[level.name] = None
                else:
                    flat_levels[level.name] = level
        return flat_levels

    def __getitem__(self, key: _LevelKey) -> _Level:
        """Return the level with the given key.

        Args:
            key: The name of the level, or a tuple like ``(hierarchy_name, level_name)``.

        Returns:
            The associated Level object

        """
        if isinstance(key, str):
            return self._find_level(None, None, key)

        if isinstance(key, tuple):
            if len(key) == 2:
                return self._find_level(None, key[0], key[1])
            if len(key) == 3:
                return self._find_level(key[0], key[1], key[2])
            raise TypeError(
                "Unexpected key of size %s, tuple must have a size of 2 or 3."
                % (len(key))
            )
        raise TypeError("Unexpected key of type %s" % (type(key)))

    def _find_level(
        self,
        dimension_name: Optional[str],
        hierarchy_name: Optional[str],
        level_name: str,
    ) -> _Level:
        """Get a level from the hierarchy name and level name."""
        if isinstance(self._hierarchies, Hierarchies):
            # pylint: disable=protected-access
            hierarchies = self._hierarchies._java_api.retrieve_hierarchy_for_level(
                self._hierarchies._cube, dimension_name, hierarchy_name, level_name
            )
            # pylint: enable=protected-access
            if len(hierarchies) > 1:
                self._raise_mutliplelevel_error(level_name, hierarchies)

            if len(hierarchies) == 0:
                raise KeyError(f"No level with name {level_name} found in cube.")

            hierarchy = hierarchies[0]

            return hierarchy.levels[level_name]

        # This is a query session and we can't use the java API.
        if dimension_name is None:
            if hierarchy_name is None:
                level = self._flatten()[level_name]
                if level:
                    return level

                return self._raise_mutliplelevel_error(
                    level_name, list(self._hierarchies.values())
                )

            return self._hierarchies[hierarchy_name][level_name]

        return self._hierarchies[(dimension_name, hierarchy_name)][level_name]

    def __iter__(self) -> Iterator[_Level]:
        """Return the iterator on all the levels."""
        return chain(
            *[iter(hierarchy.levels) for hierarchy in self._hierarchies.values()]
        )

    def __len__(self):
        """Return the number of levels."""
        return sum([len(hierarchy.levels) for hierarchy in self._hierarchies.values()])

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self._flatten())

    def _repr_json_(self) -> ReprJson:
        # Use the dimension/hierarchy/level in the map key to make it unique.
        # pylint: disable=protected-access
        data = {
            f"{lvl.name} ({lvl.dimension}/{lvl.hierarchy}/{lvl.name})": lvl._repr_json_()[
                0
            ]
            for hierarchy in self._hierarchies.values()
            for lvl in hierarchy.levels.values()
        }
        # pylint: enable=protected-access
        sorted_data = dict(sorted(data.items(), key=operator.itemgetter(0)))
        return (
            sorted_data,
            {"expanded": True, "root": "Levels",},
        )

    def _repr_html_(self) -> str:
        return convert_repr_json_to_html(self)
