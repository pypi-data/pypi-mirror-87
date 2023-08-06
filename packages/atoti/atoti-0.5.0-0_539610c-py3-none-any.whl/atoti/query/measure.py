from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QueryMeasure:
    """Measure of a query cube."""

    name: str
    """Name of the measure."""

    visible: bool
    """Whether the measure is visible or not."""

    folder: Optional[str]
    """Folder in which the measure is."""

    formatter: Optional[str]
    """Formatter of the measure."""

    description: Optional[str]
    """Description of the measure."""
