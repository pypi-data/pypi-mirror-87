from .._mappings import ImmutableMapping
from .._repr_utils import convert_repr_json_to_html, repr_json_hierarchies
from .hierarchy import QueryHierarchy


class QueryHierarchies(ImmutableMapping[str, QueryHierarchy]):
    """Manage the query hierarchies."""

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_hierarchies(self)
