from __future__ import annotations

import logging
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import pandas as pd
from typing_extensions import TypedDict

from ._context import Context
from ._discovery import Discovery, dictionarize_cube_dimensions
from .query_result import QueryResult

if TYPE_CHECKING:
    from pandas.io.formats.style import Styler

    IndexDataType = Union[str, float, int, pd.Timestamp]

LevelName = str
MeasureName = str

CubeName = str
DimensionName = str
HierarchyName = str
HierarchyCoordinates = Tuple[DimensionName, HierarchyName]
HierarchyToMaxNumberOfLevels = Mapping[HierarchyCoordinates, int]

CellMembers = Dict[HierarchyCoordinates, Sequence[str]]

MeasureValue = Optional[Union[float, int, str]]
MemberIdentifier = str
DataFrameCell = Union[MemberIdentifier, MeasureValue]
DataFrameRow = List[DataFrameCell]
DataFrameData = List[DataFrameRow]
LevelCoordinates = Tuple[DimensionName, HierarchyName, LevelName]

GetLevelDataTypes = Callable[
    [str, Collection[LevelCoordinates]], Mapping[LevelCoordinates, str]
]

SUPPORTED_DATE_FORMATS = [
    "LocalDate[yyyy-MM-dd]",
    "localDate[yyyy/MM/dd]",
    "localDate[MM-dd-yyyy]",
    "localDate[MM/dd/yyyy]",
    "localDate[dd-MM-yyyy]",
    "localDate[dd/MM/yyyy]",
    "localDate[d-MMM-yyyy]",
    "zonedDateTime[EEE MMM dd HH:mm:ss zzz yyyy]",
]

LOCAL_DATE_REGEX = re.compile(r"[lL]ocalDate\[(.*)\]")

DATE_FORMAT_MAPPING = {
    "yyyy": "%Y",
    "MM": "%m",
    "MMM": "%m",
    "dd": "%d",
    r"^d": "%d",
    "HH": "%H",
    "mm": "%M",
    "ss": "%S",
}

MEASURES_HIERARCHY: CellsetHierarchy = {
    "dimension": "Measures",
    "hierarchy": "Measures",
}
MEASURES_HIERARCHY_COORDINATES: HierarchyCoordinates = (
    MEASURES_HIERARCHY["dimension"],
    MEASURES_HIERARCHY["hierarchy"],
)


class CellsetHierarchy(TypedDict):  # noqa: D101
    dimension: DimensionName
    hierarchy: HierarchyName


class CellsetMember(TypedDict):  # noqa: D101
    # The captionPath is ignored on purpose to not repr a DataFrame index
    # containing captions that would confuse users trying to select or filter
    # members in this index.
    namePath: Sequence[MemberIdentifier]


class CellsetAxis(TypedDict):  # noqa: D101
    id: int
    hierarchies: Sequence[CellsetHierarchy]
    positions: Sequence[Sequence[CellsetMember]]


class CellsetCellProperties(TypedDict):  # noqa: D101
    BACK_COLOR: Optional[Union[int, str]]
    FONT_FLAGS: Optional[int]
    FONT_NAME: Optional[str]
    FONT_SIZE: Optional[int]
    FORE_COLOR: Optional[Union[int, str]]


class CellsetCell(TypedDict):  # noqa: D101
    formattedValue: str
    ordinal: int
    properties: CellsetCellProperties
    value: MeasureValue


class CellsetDefaultMember(TypedDict):  # noqa: D101
    dimension: DimensionName
    hierarchy: HierarchyName
    path: Sequence[MemberIdentifier]


class Cellset(TypedDict):  # noqa: D101
    axes: Sequence[CellsetAxis]
    cells: Sequence[CellsetCell]
    cube: CubeName
    defaultMembers: Sequence[CellsetDefaultMember]


def _is_slicer(axis: CellsetAxis) -> bool:
    return axis["id"] == -1


def _get_default_measure_name(cellset: Cellset) -> MeasureName:
    return next(
        member["path"][0]
        for member in cellset["defaultMembers"]
        if member["dimension"] == MEASURES_HIERARCHY["dimension"]
        and member["hierarchy"] == MEASURES_HIERARCHY["hierarchy"]
    )


def _get_measure_names(
    cellset: Cellset, default_measure_name: MeasureName
) -> Collection[str]:
    return (
        list(
            # While looping on all the positions related to the Measures axis,
            # the name of the same measure will come up repeatedly.
            # We want to keep only one occurence of each measure name and also
            # keep them in the order they appeared in the positions.
            # Since sets in Python do not preserve the order, we use a dict comprehension instead
            # since it guarantees both the uniqueness and order of its keys.
            {
                position[hierarchy_index]["namePath"][0]: None
                for axis in cellset["axes"]
                if not _is_slicer(axis)
                for hierarchy_index, hierarchy in enumerate(axis["hierarchies"])
                if hierarchy == MEASURES_HIERARCHY
                for position in axis["positions"]
            }.keys()
        )
        if cellset["axes"]
        else [
            # When there are no axes at all, there is only one cell:
            # the value of the default measure aggregated at the top.
            default_measure_name
        ]
    )


# There is a maxLevelPerHierarchy property for that in cellsets returned by the WebSocket API
# but not in those returned by the REST API that atoti uses.
def _get_hierarchy_to_max_number_of_levels(
    cellset: Cellset,
) -> HierarchyToMaxNumberOfLevels:
    hierarchy_to_max_number_of_levels: Dict[HierarchyCoordinates, int] = {}

    for axis in cellset["axes"]:
        if not _is_slicer(axis):
            for hierarchy_index, hierarchy in enumerate(axis["hierarchies"]):
                max_number_of_levels = 0
                for position in axis["positions"]:
                    number_of_levels = len(position[hierarchy_index]["namePath"])
                    if number_of_levels > max_number_of_levels:
                        max_number_of_levels = number_of_levels

                hierarchy_to_max_number_of_levels[
                    hierarchy["dimension"], hierarchy["hierarchy"]
                ] = max_number_of_levels

    return hierarchy_to_max_number_of_levels


def _get_level_coordinates(
    cellset: Cellset,
    discovery: Discovery,
    hierarchy_to_max_number_of_levels: HierarchyToMaxNumberOfLevels,
) -> Sequence[LevelCoordinates]:
    dimensions = dictionarize_cube_dimensions(
        next(
            cube
            for catalog in discovery["catalogs"]
            for cube in catalog["cubes"]
            if cube["name"] == cellset["cube"]
        )
    )

    return [
        (hierarchy["dimension"], hierarchy["hierarchy"], level["name"])
        for axis in cellset["axes"]
        if not _is_slicer(axis)
        for hierarchy in axis["hierarchies"]
        if hierarchy != MEASURES_HIERARCHY
        for level_index, level in enumerate(
            dimensions[hierarchy["dimension"]][hierarchy["hierarchy"]]["levels"]
        )
        if level_index
        < hierarchy_to_max_number_of_levels[
            hierarchy["dimension"], hierarchy["hierarchy"]
        ]
        and level["type"] != "ALL"
    ]


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-fore-color-and-back-color-contents.
# Improved over from https://github.com/activeviam/activeui/blob/ba42f1891cd6908de618fdbbab34580a6fe3ee58/packages/activeui-sdk/src/widgets/tabular/cell/MdxCellStyle.tsx#L29-L48.
def _cell_color_to_css_value(color: Union[int, str]) -> str:
    if isinstance(color, str):
        return "transparent" if color == '"transparent"' else color
    rest, red = divmod(color, 256)
    rest, green = divmod(rest, 256)
    rest, blue = divmod(rest, 256)
    return f"rgb({red}, {green}, {blue})"


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-using-cell-properties.
def _cell_font_flags_to_styles(font_flags: int) -> Collection[str]:
    styles = []
    text_decorations = []

    if font_flags & 1 == 1:
        styles.append("font-weight: bold")
    if font_flags & 2 == 2:
        styles.append("font-style: italic")
    if font_flags & 4 == 4:
        text_decorations.append("underline")
    if font_flags & 8 == 8:
        text_decorations.append("line-through")

    if text_decorations:
        styles.append(f"""text-decoration: {" ".join(text_decorations)}""")

    return styles


def _cell_properties_to_style(properties: CellsetCellProperties) -> str:
    styles = []

    back_color = properties.get("BACK_COLOR")
    if back_color is not None:
        styles.append(f"background-color: {_cell_color_to_css_value(back_color)}")

    font_flags = properties.get("FONT_FLAGS")
    if font_flags is not None:
        styles.extend(_cell_font_flags_to_styles(font_flags))

    font_name = properties.get("FONT_NAME")
    if font_name is not None:
        styles.append(f"font-family: {font_name}")

    font_size = properties.get("FONT_SIZE")
    if font_size is not None:
        styles.append(f"font-size: {font_size}px")

    fore_color = properties.get("FORE_COLOR")
    if fore_color is not None:
        styles.append(f"color: {_cell_color_to_css_value(fore_color)}")

    return "; ".join(styles)


def _get_cell_members_and_is_total(
    cell: CellsetCell,
    cellset: Cellset,
    hierarchy_to_max_number_of_levels: HierarchyToMaxNumberOfLevels,
) -> Tuple[CellMembers, bool]:
    cell_members: CellMembers = {}
    ordinal = cell["ordinal"]

    for axis in cellset["axes"]:
        if not _is_slicer(axis):
            ordinal, position_index = divmod(ordinal, len(axis["positions"]))
            for hierarchy_index, hierarchy in enumerate(axis["hierarchies"]):
                hierarchy_tuple = hierarchy["dimension"], hierarchy["hierarchy"]
                name_path = axis["positions"][position_index][hierarchy_index][
                    "namePath"
                ]

                if len(name_path) == hierarchy_to_max_number_of_levels[hierarchy_tuple]:
                    cell_members[hierarchy_tuple] = tuple(
                        name for name in name_path if name != "AllMember"
                    )
                else:
                    return {}, True

    return cell_members, False


def _format_to_pandas_type(
    value_type: str, values: Collection[Any]
) -> Collection[IndexDataType]:
    """Format values to a specific pandas data type.

    Formatted value can be a date, int, float or object.
    """
    if value_type in ["int", "float"]:
        return pd.to_numeric(values)
    if value_type in SUPPORTED_DATE_FORMATS:
        try:
            if value_type.lower().startswith("localdate["):
                date_format = LOCAL_DATE_REGEX.match(value_type).groups()[0]  # type: ignore
                for regex, value in DATE_FORMAT_MAPPING.items():
                    date_format = re.sub(regex, value, date_format)
                return pd.to_datetime(values, format=date_format)
            if value_type.startswith("zonedDateTime["):
                return pd.to_datetime(values)
        except ValueError as err:
            logging.getLogger("atoti.query").warning(
                "Failed to convert type %s to a pandas date, using string instead. %s",
                value_type,
                err,
            )
    return values


def _get_index(
    cellset: Cellset,
    levels_coordinates: Sequence[LevelCoordinates],
    members: Iterable[Tuple[str, ...]],
    get_level_data_types: Optional[GetLevelDataTypes] = None,
) -> Optional[pd.Index]:
    if not levels_coordinates:
        return None

    index_dataframe = pd.DataFrame(
        members,
        columns=[level_coordinates[2] for level_coordinates in levels_coordinates],
    )
    level_data_types = (
        get_level_data_types(cellset["cube"], levels_coordinates)
        if get_level_data_types
        else {level_coordinates: "object" for level_coordinates in levels_coordinates}
    )
    for level_coordinates in levels_coordinates:
        level_name = level_coordinates[2]
        index_dataframe[level_name] = _format_to_pandas_type(
            level_data_types[level_coordinates], index_dataframe[level_name]
        )

    if len(levels_coordinates) == 1:
        return pd.Index(index_dataframe[levels_coordinates[0][2]])

    return pd.MultiIndex.from_frame(index_dataframe)


def _create_measure_collection(
    measure_values: Collection[Mapping[str, Any]],
    index: pd.Index,  # type: ignore
    measure_name: str,
) -> Union[Collection[MeasureValue], pd.Series]:
    values = [values.get(measure_name) for values in measure_values]
    return (
        pd.Series(
            values,
            # Forcing `object` dtypes when some measure values are ``None`` to prevent pandas from inferring a numerical type and ending up with NaNs.
            dtype="object",
            index=index,
        )
        if None in values
        else values
    )


def _get_data_values(
    measure_values: Collection[Mapping[str, Any]],
    index: pd.Index,  # type: ignore
    measure_names: Collection[str],
) -> Mapping[str, Union[Collection[MeasureValue], pd.Series]]:
    """Return a mapping of collection where the dtype is ``object`` when some measure values are ``None``."""
    return {
        measure_name: _create_measure_collection(measure_values, index, measure_name)
        for measure_name in measure_names
    }


def cellset_to_query_result(
    cellset: Cellset,
    discovery: Discovery,
    *,
    context: Optional[Context] = None,
    get_level_data_types: Optional[GetLevelDataTypes] = None,
    mdx: Optional[str] = None,
) -> pd.DataFrame:
    """Convert an MDX cellset to a pandas DataFrame.

    Args:
        cellset: The MDX cellset.
        discovery: The discovery of the corresponding server.
        context: The context values of the corresponding query.
        get_level_data_types: Return the list of types matching the list of level names.
        mdx: The mdx of the corresponding query.
    """
    default_measure_name = _get_default_measure_name(cellset)
    hierarchy_to_max_number_of_levels = _get_hierarchy_to_max_number_of_levels(cellset)

    has_some_style = next(
        (True for cell in cellset["cells"] if cell["properties"]), False
    )

    members_to_measure_formatted_values = {}
    members_to_measure_styles = {}
    members_to_measure_values = {}

    for cell in cellset["cells"]:
        cell_members, is_total = _get_cell_members_and_is_total(
            cell, cellset, hierarchy_to_max_number_of_levels
        )

        if not is_total:
            measure_name = cell_members.setdefault(
                MEASURES_HIERARCHY_COORDINATES, [default_measure_name],
            )[0]

            member = tuple(
                name
                for hierarchy, cell_member in cell_members.items()
                if hierarchy != MEASURES_HIERARCHY_COORDINATES
                for name in cell_member
            )

            members_to_measure_values.setdefault(member, {})[measure_name] = cell[
                "value"
            ]
            members_to_measure_formatted_values.setdefault(member, {})[
                measure_name
            ] = cell["formattedValue"]

            if has_some_style:
                members_to_measure_styles.setdefault(member, {})[
                    measure_name
                ] = _cell_properties_to_style(cell["properties"])

    levels_coordinates = _get_level_coordinates(
        cellset, discovery, hierarchy_to_max_number_of_levels
    )

    index = _get_index(
        cellset,
        levels_coordinates,
        members_to_measure_values.keys(),
        get_level_data_types,
    )

    measure_names = _get_measure_names(cellset, default_measure_name)

    formatted_values_dataframe = pd.DataFrame(
        members_to_measure_formatted_values.values(),
        index,
        measure_names,
        dtype="string",
    )

    def _get_styler() -> Styler:
        styler = formatted_values_dataframe.style

        if has_some_style:
            styler = styler.apply(
                lambda _: pd.DataFrame(
                    members_to_measure_styles.values(), index, measure_names,
                ),
                axis=None,
            )

        return styler

    return QueryResult(
        _get_data_values(members_to_measure_values.values(), index, measure_names),
        index,
        context=context,
        formatted_values=formatted_values_dataframe,
        get_styler=_get_styler,
        mdx=mdx,
    )
