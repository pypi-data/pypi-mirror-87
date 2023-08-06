from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Union, cast

if TYPE_CHECKING:
    from .cube import Cube
    from .cubes import Cubes
    from .experimental.distributed.cubes import DistributedCube, DistributedCubes
    from .experimental.distributed.hierarchies import DistributedHierarchies
    from .experimental.distributed.measures import DistributedMeasures
    from .experimental.distributed.session import DistributedSession
    from .hierarchies import Hierarchies
    from .hierarchy import Hierarchy
    from .measures import Measures
    from .query.cube import QueryCube
    from .query.cubes import QueryCubes
    from .query.hierarchies import QueryHierarchies
    from .query.hierarchy import QueryHierarchy
    from .query.measures import QueryMeasures
    from .query.session import QuerySession
    from .session import Session

_INDENTATION = "  "

ReprJson = Tuple[Any, Dict[str, Union[bool, str]]]


def _json_to_html(obj: Union[List[Any], Dict[str, Any]], indent: int = 0) -> str:
    return (
        _list_to_html(obj, indent)
        if isinstance(obj, list)
        else _dict_to_html(obj, indent)
    )


def _dict_to_html(dic: Dict[str, Any], indent: int = 0) -> str:
    pretty = f"{_INDENTATION * indent}<ul>\n"
    for key, value in dic.items():
        if isinstance(value, (dict, list)):
            pretty += f"{_INDENTATION * indent}<li>{key}\n"
            pretty += _json_to_html(value, indent + 1)
            pretty += f"{_INDENTATION * indent}</li>\n"
        else:
            pretty += f"{_INDENTATION * indent}<li>{key}: {value}</li>\n"
    return f"{pretty}{_INDENTATION * indent}</ul>\n"


def _list_to_html(lis: List[Any], indent: int = 0) -> str:
    pretty = f"{_INDENTATION * indent}<ol>\n"
    for value in lis:
        if isinstance(value, (dict, list)):
            pretty += (
                f"{_INDENTATION * indent}<li>{_json_to_html(value, indent + 1)}</li>\n"
            )
        else:
            pretty += f"{_INDENTATION * indent}<li>{value}</li>\n"
    return f"{pretty}{_INDENTATION * indent}</ol>"


def convert_repr_json_to_html(obj: Any) -> str:
    """Convert the JSON repr to HTML.

    Args:
        obj: An object with a ``_repr_json_`` method.
    """
    repr_json = obj._repr_json_()
    metadata = repr_json[1]
    if "root" in metadata:
        obj = {repr_json[1]["root"]: repr_json[0]}
    else:
        obj = repr_json[0]
    return _json_to_html(obj)


def repr_json_cubes(cubes: Union[Cubes, QueryCubes, DistributedCubes]) -> ReprJson:
    """Return the JSON representation of cubes."""
    return (
        {name: cube._repr_json_()[0] for name, cube in sorted(cubes.items())},
        {"expanded": False, "root": "Cubes"},
    )


def repr_json_cube(cube: Union[Cube, QueryCube, DistributedCube]) -> ReprJson:
    """Return the JSON representation of a cube."""
    return (
        {
            "Dimensions": cube.hierarchies._repr_json_()[0],
            "Measures": cube.measures._repr_json_()[0],
        },
        {"expanded": False, "root": cube.name},
    )


def repr_json_hierarchies(
    hierarchies: Union[Hierarchies, QueryHierarchies, DistributedHierarchies]
) -> ReprJson:
    """Return the JSON representation of hierarchies."""
    dimensions = dict()
    for hierarchy in hierarchies.values():
        dimensions.setdefault(hierarchy.dimension, []).append(hierarchy)
    json = {
        dimension: dict(
            sorted(
                {
                    hierarchy._repr_json_()[1]["root"]: hierarchy._repr_json_()[0]
                    for hierarchy in dimension_hierarchies
                }.items()
            )
        )
        for dimension, dimension_hierarchies in sorted(dimensions.items())
    }
    return json, {"expanded": True, "root": "Dimensions"}


def repr_json_hierarchy(hierarchy: Union[Hierarchy, QueryHierarchy]) -> ReprJson:
    """Return the JSON representation of a hierarchy."""
    root = f"{hierarchy.name}{' (slicing)' if hierarchy.slicing else ''}"
    return (
        [level.name for level in hierarchy.levels.values()],
        {"root": root, "expanded": False,},
    )


def repr_json_measures(
    measures: Union[Measures, QueryMeasures, DistributedMeasures]
) -> ReprJson:
    """Return the JSON representation of measures."""
    measures_json = dict()
    no_folder = dict()
    for measure in measures.values():
        if measure.visible:
            json = {"formatter": measure.formatter}
            if measure.description is not None:
                json["description"] = measure.description
            if measure.folder is None:
                # We store them into another dict to insert them after the folders
                no_folder[measure.name] = json
            else:
                folder = f"📁 {measure.folder}"
                measures_json.setdefault(folder, {})[measure.name] = json
    for folder, measures_in_folder in measures_json.items():
        measures_json[folder] = dict(sorted(measures_in_folder.items()))
    return (
        {**measures_json, **dict(sorted(no_folder.items()))},
        {"expanded": False, "root": "Measures"},
    )


def repr_json_session(
    session: Union[Session, DistributedSession, QuerySession]
) -> ReprJson:
    """Return the JSON representation of a session."""
    cubes = session.cubes._repr_json_()[0]
    data = (
        {"Stores": cast(Any, session).stores._repr_json_()[0], "Cubes": cubes}
        if hasattr(session, "stores")
        else {"Cubes": cubes}
    )
    return (
        data,
        {"expanded": False, "root": session.name},
    )
