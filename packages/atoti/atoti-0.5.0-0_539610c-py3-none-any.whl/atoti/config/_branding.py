from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from shutil import copyfile
from typing import Any, Mapping, Optional, Union

from .._file_utils import _make_atoti_tempir
from .._path_utils import to_absolute_path
from ._utils import Configuration


@dataclass(frozen=True)
class Branding(Configuration):

    accent_color: Optional[str]
    favicon: Optional[Union[Path, str]]
    frame_color: Optional[str]
    logo: Optional[Union[Path, str]]
    title: Optional[str]

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        return create_branding(**data)


def _create_branding_directory(branding: Branding) -> str:
    tmpdir = Path(_make_atoti_tempir())
    if branding.favicon:
        copyfile(to_absolute_path(branding.favicon), tmpdir / "favicon.ico")
    if branding.logo:
        copyfile(to_absolute_path(branding.logo), tmpdir / "logo.svg")
    (tmpdir / "branding.js").write_text(
        f"""window._atotiBranding = {json.dumps({
        "accentColor": branding.accent_color,
        "frameColor": branding.frame_color,
        "title": branding.title,
    })};"""
    )
    return to_absolute_path(tmpdir)


def create_branding(
    *,
    accent_color: Optional[str] = None,
    favicon: Optional[Union[Path, str]] = None,
    frame_color: Optional[str] = None,
    logo: Optional[Union[Path, str]] = None,
    title: Optional[str] = None,
) -> Branding:
    """Create an application branding configuration.

    Args:
        accent_color: The CSS color to give to hovered elements of the frame (header and sidenav).
        favicon: The file path to the ``.ico`` image to use as the favicon.
        frame_color: The CSS color to give to the background of the frame (header and sidenav).
        logo: The file path to the ``.svg`` image that will be displayed in a 24px by 24px area in the upper-left corner.
        title: The title to give to the page.
    """
    return Branding(
        favicon=str(favicon.absolute()) if isinstance(favicon, Path) else favicon,
        accent_color=accent_color,
        frame_color=frame_color,
        logo=str(logo.absolute()) if isinstance(logo, Path) else logo,
        title=title,
    )
