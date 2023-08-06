from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Callable, Dict, Mapping, Optional

import pandas as pd

from .._version import VERSION
from ._context import Context

if TYPE_CHECKING:
    from pandas.io.formats.style import Styler

# Similar naming scheme as our widgets:
_QUERY_RESULT_MIME_TYPE = (
    f"application/vnd.atoti.query-result.v{VERSION.split('.')[0]}+json"
)


class QueryResult(pd.DataFrame):  # pylint: disable=abstract-method
    """Custom pandas DataFrame that can be converted to a widget by our JupyterLab extension."""

    # See https://pandas.pydata.org/pandas-docs/stable/development/extending.html#define-original-properties
    _internal_names = pd.DataFrame._internal_names + [
        "_atoti_context",
        "_atoti_create_equivalent_widget_code",
        "_atoti_formatted_values",
        "_atoti_get_styler",
        "_atoti_has_changed",
        "_atoti_initial_dataframe",
        "_atoti_mdx",
    ]
    _internal_names_set = set(_internal_names)

    def __init__(
        self,
        # pandas does not expose the types of these arguments so we use Any instead.
        data: Any = None,
        index: Any = None,
        *,
        context: Optional[Context] = None,
        formatted_values: pd.DataFrame,  # type: ignore
        get_styler: Callable[[], Styler],  # type: ignore
        mdx: Optional[str] = None,
    ):
        """Init the parent DataFrame and set extra internal attributes."""
        super().__init__(data, index)  # type: ignore
        self._atoti_context = context
        self._atoti_create_equivalent_widget_code: Optional[str] = None
        self._atoti_formatted_values = formatted_values
        self._atoti_get_styler = get_styler
        self._atoti_has_changed = False
        self._atoti_initial_dataframe = self.copy(deep=True)
        self._atoti_mdx = mdx

    # The conversion to an atoti widget and the styling are based on the fact
    # that this dataframe represents the original result of an MDX query.
    # If the dataframe was mutated in place, these features should be disabled
    # to prevent them from being incorrect.
    def _has_changed(self):
        if not self._atoti_has_changed:
            if not self.equals(self._atoti_initial_dataframe):
                self._atoti_has_changed = True

                logging.getLogger("atoti.query").warning(
                    "The query result has been changed in place, formatted values and styling will not be shown."
                )

        return self._atoti_has_changed

    @property
    def style(self) -> Styler:
        """Return a Styler object.

        If the DataFrame has not been changed in place since its creation, the returned object will follow the styling included in the cellset from which the DataFrame was converted.
        """
        return (
            super().style
            if self._has_changed()
            else self._atoti_get_styler()
            # Keep the original class used in the selector of our "Convert to atoti Widget Below" command.
        ).set_table_attributes('class="dataframe"')

    def _get_dataframe_to_repr(self, has_changed: bool) -> pd.DataFrame:  # type: ignore
        return super() if has_changed else self._atoti_formatted_values

    def _atoti_repr(self, has_changed: bool) -> str:
        return self._get_dataframe_to_repr(has_changed).__repr__()

    def __repr__(self) -> str:  # noqa: D105
        return self._atoti_repr(self._has_changed())

    def _atoti_repr_html(self, has_changed: bool) -> str:
        return self._get_dataframe_to_repr(has_changed)._repr_html_()

    def _repr_html_(self) -> str:
        return self._atoti_repr_html(self._has_changed())

    def _atoti_repr_latex(self, has_changed: bool) -> str:
        return self._get_dataframe_to_repr(has_changed)._repr_latex_()

    def _repr_latex_(self) -> str:
        return self._atoti_repr_latex(self._has_changed())

    def _repr_mimebundle_(
        self, include: Any, exclude: Any  # pylint: disable=unused-argument
    ) -> Mapping[str, Any]:
        has_changed = self._has_changed()

        mimebundle: Dict[str, Any] = {
            "text/html": self._atoti_repr_html(has_changed),
            "text/plain": self._atoti_repr(has_changed),
        }

        if self._atoti_create_equivalent_widget_code and not has_changed:
            mimebundle[_QUERY_RESULT_MIME_TYPE] = {
                "context": self._atoti_context,
                "createEquivalentWidgetCode": self._atoti_create_equivalent_widget_code,
                "mdx": self._atoti_mdx,
            }

        return mimebundle
