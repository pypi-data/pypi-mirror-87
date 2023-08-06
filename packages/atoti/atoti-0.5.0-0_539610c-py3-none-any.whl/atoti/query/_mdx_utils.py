from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Set, Union

from .._hierarchy_isin_conditions import HierarchyIsInCondition
from .._level_conditions import LevelCondition
from .._level_isin_conditions import LevelIsInCondition
from .._type_utils import BASE_SCENARIO, ScenarioName
from .hierarchy import QueryHierarchy
from .level import QueryLevel
from .measure import QueryMeasure

if TYPE_CHECKING:
    from ..level import Level
    from .cube import QueryCube


def __parse_name(name: str) -> str:
    """Deal with special characters.

    ``]`` must become ``]]``

    """
    if "]" in name:
        name = name.replace("]", "]]")
    return name


def _keep_only_deepest_levels(
    cube: QueryCube, levels: Sequence[QueryLevel],
) -> Sequence[QueryLevel]:
    shallow_levels: Set[QueryLevel] = set()
    hierarchy_to_deepest_level: Dict[str, QueryLevel] = dict()
    for level in levels:
        deepest_level = hierarchy_to_deepest_level.get(level.hierarchy)
        if deepest_level:
            # This relies on the fact that dicts are ordered.
            hierarchy_levels = list(cube.hierarchies[level.hierarchy].levels.values())
            still_deepest_level = hierarchy_levels.index(
                deepest_level
            ) > hierarchy_levels.index(level)
            if still_deepest_level:
                shallow_levels.add(level)
            else:
                shallow_levels.add(deepest_level)
                hierarchy_to_deepest_level[level.hierarchy] = level
        else:
            hierarchy_to_deepest_level[level.hierarchy] = level
    return [level for level in levels if level not in shallow_levels]


def _generate_mdx_level_members(level: QueryLevel) -> str:
    """Generate a string describing a level such as ``[dimension][hierarchy][level_name].Members``."""
    return (
        f"[{__parse_name(level.dimension)}]."
        f"[{__parse_name(level.hierarchy)}]."
        f"[{__parse_name(level.name)}].Members"
    )


def _generate_mdx_condition_member(
    hierarchy: QueryHierarchy,
    level: Union[QueryLevel, Level],
    value: Any,
    operation: str,
) -> str:
    """Generate a string describing a filter on level.

    Args:
        hierarchy: hierarchy of the level
        level: the level to filter on
        value: the value used in the condition
        operation: the operation used in the condition
    Returns:
        a string like [dimension][hierarchy].[ALL].[AllMember].[{value}]
    """
    if operation != "eq":
        raise (
            ValueError(
                f"'{operation}' not supported:"
                " level conditions can only be based on equality (==)."
            )
        )
    if not isinstance(value, str):
        raise (
            TypeError(
                f"Type '{type(value)}' not supported:"
                " level conditions can only be based on equality with strings."
            )
        )
    return (
        (
            f"[{__parse_name(hierarchy.dimension)}]."
            f"[{__parse_name(hierarchy.name)}]."
            f"[ALL].[AllMember].[{__parse_name(value)}]"
        )
        if not hierarchy.slicing
        else (
            f"[{__parse_name(hierarchy.dimension)}]."
            f"[{__parse_name(hierarchy.name)}]."
            f"[{__parse_name(level.name)}].[{__parse_name(value)}]"
        )
    )


def _generate_mdx_hierarchy_isin_member(
    hierarchy: QueryHierarchy, values: List[str],
) -> str:
    """Generate a string describing a filter on hierarchy levels.

    Args:
        hierarchy: hierarchy of the level
        values: the list of values used in the condition
    Returns:
        a string like [dimension][hierarchy].[ALL].[AllMember].[value1].[value2]
    """
    temp = []
    for value in values:
        if not isinstance(value, str):
            raise (
                TypeError(
                    f"Type '{type(values)}' not supported:"
                    " level conditions can only be based on equality with strings."
                )
            )
        temp.append(f"[{__parse_name(value)}]")

    string = ".".join(temp)
    return (
        f"[{__parse_name(hierarchy.dimension)}]."
        f"[{__parse_name(hierarchy.name)}].[ALL].[AllMember]."
        f"{string}"
    )


def _generate_mdx_scenario_members(scenario_name: ScenarioName) -> str:
    """Generate a string describing a Scenario.

    Args:
        scenario: scenario name you want to query on

    Returns:
        a string like [Epoch].[Epoch].[Branch].[scenario_name]
    """
    return f"[Epoch].[Epoch].[Branch].[{__parse_name(scenario_name)}]"


def _generate_columns_set(measures: Optional[Sequence[QueryMeasure]] = None) -> str:
    """Generate a string describing Columns query.

    Args:
        measures: List of measures

    Returns:
        [Measures].AllMembers or
        [Measures].[measure_name] or
        {[Measures].[measure_name],[Measures].[measure_name],...}
        Depending on the number of measures given as arguments
    """
    if not measures:
        return "[Measures].AllMembers"
    if len(measures) == 1:
        return f"[Measures].[{__parse_name(measures[0].name)}]"
    measures_list_string = ",".join(
        [f"[Measures].[{__parse_name(measure.name)}]" for measure in measures]
    )
    return f"{{{measures_list_string}}}"


def _generate_rows_set(levels: Sequence[QueryLevel]) -> str:
    """Generate a string describing rows query.

    Args:
        levels: List of levels

    Returns:
        [dimension].[hierarchy].[level_name].Members or
        Crossjoin([dimension].[hierarchy].[level_name].Members,...)
        Depending on the number of levels given as arguments
    """
    if len(levels) == 1:
        return _generate_mdx_level_members(levels[0])
    mdx_description_levels = ",".join(
        [_generate_mdx_level_members(level) for level in levels]
    )
    return f"Crossjoin({mdx_description_levels})"


def _generate_from_set(
    cube: QueryCube,
    hierarchy_conditions: Dict[str, List[Union[LevelCondition, Dict[str, Any]]]],
) -> str:
    """Generate FROM mdx request depending on filters.

    Args:
        cube: the cube to query
        hierarchy_conditions: dict of hierachy name to level condition
    """
    if hierarchy_conditions:
        # pylint: disable=protected-access
        conditions = ",".join(
            [
                f"""{{{",".join(
                    [
                        _generate_mdx_condition_member(
                            cube.hierarchies[condition._level.hierarchy],
                            condition._level,
                            condition._value,
                            condition._operation,
                        )
                        if isinstance(condition, LevelCondition)
                        else _generate_mdx_hierarchy_isin_member(
                            condition["hierarchy"], condition["values"],
                        )
                        for condition in hierarchy_subdict
                    ]
                )}}}"""
                for hierarchy_subdict in hierarchy_conditions.values()
            ]
        )
        # pylint: enable=protected-access
        return (
            f"FROM (SELECT ({conditions}) ON COLUMNS FROM [{__parse_name(cube.name)}])"
        )
    return f"FROM [{__parse_name(cube.name)}]"


def generate_mdx(
    cube: QueryCube,
    measures: Sequence[QueryMeasure],
    levels: Sequence[QueryLevel],
    scenario: ScenarioName,
    conditions: Sequence[LevelCondition],
    level_isin_conditions: Sequence[LevelIsInCondition],
    hierarchy_isin_conditions: Sequence[HierarchyIsInCondition],
) -> str:
    """Generate MDX query string.

    The value of the measures is given on all the members of the given levels.
    If no measure is specified then all the measures are returned.
    If no level is specified then the value at the top level is returned

    Args:
        cube: the cube to query.
        measures: the measures to query.
        levels: the levels to split on.
        scenario: the scenario to query.
        conditions: filtering conditions to apply.

    Returns:
        The resulting MDX query.

    """
    deepest_levels = _keep_only_deepest_levels(cube, levels)
    # dict for LevelConditions
    hierarchy_conditions: Dict[str, List[Union[LevelCondition, Dict[str, Any]]]] = {}
    # pylint: disable=protected-access
    for condition in conditions:
        hierarchy_conditions.setdefault(condition._level.hierarchy, []).append(
            condition
        )
    for condition in level_isin_conditions:
        for value in condition._members:
            hierarchy_conditions.setdefault(condition._level.hierarchy, []).append(
                condition._level == value
            )
    for condition in hierarchy_isin_conditions:
        for subdict in condition._members:
            hierarchy_conditions.setdefault(condition._hierarchy.name, []).append(
                {"values": list(subdict.values()), "hierarchy": condition._hierarchy,}
            )
    # pylint: enable=protected-access
    mdx = f"SELECT {_generate_columns_set(measures)} ON COLUMNS"
    mdx += (
        f", NON EMPTY {_generate_rows_set(deepest_levels)} ON ROWS"
        if deepest_levels
        else ""
    )
    mdx += f" {_generate_from_set(cube, hierarchy_conditions)}"

    if scenario != BASE_SCENARIO:
        mdx += f" WHERE {_generate_mdx_scenario_members(scenario)}"
    return mdx
