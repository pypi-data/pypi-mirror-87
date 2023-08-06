import json
from typing import Any, Mapping, Optional, Union
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .._docs_utils import doc
from .._repr_utils import convert_repr_json_to_html, repr_json_session
from ._cellset import Cellset, cellset_to_query_result
from ._context import Context
from ._discovery import Discovery
from ._discovery_utils import create_cubes_from_discovery
from .auth import Auth
from .cubes import QueryCubes
from .query_result import QueryResult

SUPPORTED_VERSIONS = ["5", "5.Z1", "4"]

_QUERY_MDX_ARGS = """Args:
            mdx: The MDX ``SELECT`` query to execute.
            timeout: The query timeout in seconds.
"""

_QUERY_MDX_DOC = f"""Execute an MDX query and return its result as a pandas DataFrame.

        Resulting cells representing totals are ignored, they will not be part of the returned DataFrame.
        Members for which all the measures are ``None`` are ignored too.

        Example:

            An MDX query that would be displayed as this pivot table:

            +---------------+-----------------+------------+------------+------------+------------+
            | Country       | Total Price.SUM | 2018-01-01 | 2019-01-01 | 2019-01-02 | 2019-01-05 |
            |               |                 +------------+------------+------------+------------+
            |               |                 | Price.SUM  | Price.SUM  | Price.SUM  | Price.SUM  |
            +---------------+-----------------+------------+------------+------------+------------+
            | Total Country |        2,280.00 |     840.00 |   1,860.00 |     810.00 |     770.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | China         |          760.00 |            |            |     410.00 |     350.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | France        |        1,800.00 |     480.00 |     500.00 |     400.00 |     420.00 |
            +---------------+-----------------+------------+------------+------------+------------+
            | India         |          760.00 |     360.00 |     400.00 |            |            |
            +---------------+-----------------+------------+------------+------------+------------+
            | UK            |          960.00 |            |     960.00 |            |            |
            +---------------+-----------------+------------+------------+------------+------------+

            will return this DataFrame:

            +------------+---------+-----------+
            | Date       | Country | Price.SUM |
            +============+=========+===========+
            | 2019-01-02 | China   | 410.0     |
            +------------+---------+-----------+
            | 2019-01-05 | China   | 350.0     |
            +------------+---------+-----------+
            | 2018-01-01 | France  | 480.0     |
            +------------+---------+-----------+
            | 2019-01-01 | France  | 500.0     |
            +------------+---------+-----------+
            | 2019-01-02 | France  | 400.0     |
            +------------+---------+-----------+
            | 2019-01-05 | France  | 420.0     |
            +------------+---------+-----------+
            | 2018-01-01 | India   | 360.0     |
            +------------+---------+-----------+
            | 2019-01-01 | India   | 400.0     |
            +------------+---------+-----------+
            | 2019-01-01 | UK      | 960.0     |
            +------------+---------+-----------+


        {_QUERY_MDX_ARGS}
"""


class QuerySession:
    """Used to query an existing session.

    Query sessions are considered immutable: the structure of their cubes is not expected to change.
    """

    def __init__(
        self, url: str, *, auth: Optional[Auth] = None, name: Optional[str] = None
    ):
        """Init.

        Args:
            url: The server base URL.
            auth: The authentication to use.
            name: The name to give to the session.
        """
        from .._plugins import get_active_plugins

        self._url = url
        self._name = name or url
        self._auth = auth or (lambda url: None)
        self._version = self._fetch_version()
        self._discovery = self._fetch_discovery()
        self._cubes = create_cubes_from_discovery(self._discovery, self)
        plugins = get_active_plugins()
        for plugin in plugins:
            plugin.init_query_session(self)

    @property
    def cubes(self) -> QueryCubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    def url(self) -> str:
        """URL of the session."""
        return self._url

    @property
    def port(self) -> Optional[int]:
        """Port of the session."""
        return urlparse(self.url).port

    # pylint: disable=unused-argument
    def visualize(self, *args: Any, **kwargs: Any):  # pylint: disable=no-self-use
        """atoti-jupyterlab is required."""
        from .._plugins import MissingPluginError

        raise MissingPluginError("jupyterlab")

    # pylint: enable=unused-argument

    def _generate_auth_headers(self) -> Mapping[str, str]:
        """Generate the authentication headers to use for this session."""
        return self._auth(self.url) or {}

    def _execute_json_request(self, url: str, body: Optional[Any] = None) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self._auth(url) or {})
        data = json.dumps(body).encode("utf8") if body else None
        # The user can send any URL, wrapping it in a request object makes it a bit safer
        request = Request(url, data=data, headers=headers)
        try:
            response = urlopen(request)  # nosec
            return json.load(response)
        except HTTPError as error:
            error_json = error.read()
            error_data = json.loads(error_json)
            raise RuntimeError("Request failed", error_data) from error

    def _fetch_version(self) -> str:
        url = f"{self._url}/versions/rest"
        response = self._execute_json_request(url)
        exposed_versions = [
            version["id"] for version in response["apis"]["pivot"]["versions"]
        ]
        try:
            return next(
                version for version in SUPPORTED_VERSIONS if version in exposed_versions
            )
        except Exception:
            raise RuntimeError(
                f"Exposed versions: {exposed_versions}"
                f" don't match supported ones: {SUPPORTED_VERSIONS}"
            ) from None

    def _fetch_discovery(self) -> Discovery:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/discovery"
        response = self._execute_json_request(url)
        return response["data"]

    def _query_mdx_to_cellset(self, mdx: str, context: Context) -> Cellset:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/query/mdx"
        body: Mapping[str, Union[str, Context]] = {"context": context, "mdx": mdx}
        response = self._execute_json_request(url, body)
        return response["data"]

    @doc(_QUERY_MDX_DOC)
    def query_mdx(self, mdx: str, *, timeout: int = 30, **kwargs: Any,) -> QueryResult:
        # We use kwargs to hide uncommon features from the public API.
        context: Context = kwargs.get("context", {})
        if timeout is not None:
            context = {**context, "queriesTimeLimit": timeout}
        cellset = self._query_mdx_to_cellset(mdx, context)
        query_result = cellset_to_query_result(
            cellset,
            self._discovery,
            context=context,
            get_level_data_types=kwargs.get("get_level_data_types"),
            mdx=mdx,
        )
        return query_result

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_session(self)
