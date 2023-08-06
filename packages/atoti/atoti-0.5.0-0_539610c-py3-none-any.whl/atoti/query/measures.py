from .._mappings import ImmutableMapping
from .._repr_utils import convert_repr_json_to_html, repr_json_measures
from .measure import QueryMeasure


class QueryMeasures(ImmutableMapping[str, QueryMeasure]):
    """Manage the query measures."""

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_measures(self)
