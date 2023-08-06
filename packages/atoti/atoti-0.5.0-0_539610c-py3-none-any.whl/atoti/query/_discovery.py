from __future__ import annotations

from typing import List, Mapping, Optional

from typing_extensions import TypedDict

LevelName = str
MeasureName = str

CubeName = str
DimensionName = str
HierarchyName = str

MemberIdentifier = str


class DiscoveryLevel(TypedDict):  # noqa: D101
    name: str
    type: str


class DiscoveryHierarchy(TypedDict):  # noqa: D101
    levels: List[DiscoveryLevel]
    name: HierarchyName
    slicing: bool


class DiscoveryDimension(TypedDict):  # noqa: D101
    hierarchies: List[DiscoveryHierarchy]
    name: DimensionName


class DiscoveryMeasure(TypedDict):  # noqa: D101
    name: DimensionName
    visible: bool
    folder: Optional[str]
    formatter: Optional[str]
    description: Optional[str]


class DiscoveryCube(TypedDict):  # noqa: D101
    dimensions: List[DiscoveryDimension]
    measures: List[DiscoveryMeasure]
    name: CubeName


class DiscoveryCatalog(TypedDict):  # noqa: D101
    cubes: List[DiscoveryCube]


class Discovery(TypedDict):  # noqa: D101
    catalogs: List[DiscoveryCatalog]


DiscoveryHierarchyDict = Mapping[HierarchyName, DiscoveryHierarchy]
DiscoveryDimensionDict = Mapping[DimensionName, DiscoveryHierarchyDict]


def _dictionarize_dimension_hierarchies(
    dimension: DiscoveryDimension,
) -> DiscoveryHierarchyDict:
    """Make access to hierarchy by name more efficient."""
    return {hierarchy["name"]: hierarchy for hierarchy in dimension["hierarchies"]}


def dictionarize_cube_dimensions(cube: DiscoveryCube) -> DiscoveryDimensionDict:
    """Make access to dimension by name more efficient."""
    return {
        dimension["name"]: _dictionarize_dimension_hierarchies(dimension)
        for dimension in cube["dimensions"]
    }
