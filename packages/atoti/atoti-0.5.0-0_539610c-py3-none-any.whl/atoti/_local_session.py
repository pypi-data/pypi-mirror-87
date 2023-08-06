from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Mapping,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
)

from typing_extensions import Literal

from ._docs_utils import doc
from ._endpoint import PyApiEndpoint
from ._ipython_utils import run_from_ipython
from ._java_api import JavaApi
from ._path_utils import stem_path
from ._plugins import MissingPluginError, get_active_plugins
from ._query_plan import QueryAnalysis
from ._repr_utils import convert_repr_json_to_html
from ._server_subprocess import ServerSubprocess
from ._type_utils import Port, typecheck
from ._vendor.atotipy4j.java_gateway import DEFAULT_PORT as _PY4J_DEFAULT_PORT
from .config import SessionConfiguration
from .config._branding import _create_branding_directory
from .exceptions import AtotiException, AtotiJavaException
from .logs import Logs
from .query.query_result import QueryResult
from .query.session import _QUERY_MDX_ARGS, _QUERY_MDX_DOC

if TYPE_CHECKING:
    from ._endpoint import CallbackEndpoint
    from ._repr_utils import ReprJson
    from .cubes import Cubes
    from .experimental.distributed.cubes import DistributedCubes
    from .query.session import QuerySession

    _Cubes = TypeVar("_Cubes", Cubes, DistributedCubes)

_CubeCreationMode = Literal[  # pylint: disable=invalid-name
    "auto", "manual", "no_measures"
]


def _resolve_metadata_db(metadata_db: str) -> str:
    if metadata_db.startswith("jdbc"):
        raise NotImplementedError("jdbc URLs are not yet supported.")

    # Remote URL don't need to be resolved
    if metadata_db.startswith("http://") or metadata_db.startswith("https://"):
        return metadata_db

    # Make sure the parent directory exists.
    path = Path(metadata_db)
    if path.exists() and not path.is_dir():
        raise ValueError(f"metadata_db is not a directory: {metadata_db}")
    path.mkdir(exist_ok=True)

    # Return the fully resolved path.
    return str(path.resolve())


def _find_corresponding_top_level_variable_name(value: Any) -> Optional[str]:
    from IPython import get_ipython

    top_level_variables: Mapping[str, Any] = cast(Any, get_ipython()).user_ns

    for variable_name, variable_value in top_level_variables.items():
        is_regular_variable = not variable_name.startswith("_")
        if is_regular_variable and variable_value is value:
            return variable_name

    return None


def _infer_store_name(path: Union[Path, str], store_name: Optional[str]) -> str:
    """Infer the name of a store given the path and store_name parameters."""
    return store_name or stem_path(path).capitalize()


@typecheck
class ALocalSession(ABC):
    """Abstract session class."""

    def __init__(
        self,
        name: str,
        config: SessionConfiguration,
        distributed: bool = False,
        **kwargs: Any,
    ):
        """Init."""
        self._name = name
        self._config = config

        self._create_subprocess_and_java_api(
            distributed, **kwargs,
        )

        try:
            self._configure_session()
        except AtotiJavaException as ave:
            # Raise an exception if the session configuration fails
            raise AtotiException(
                f"{ave.java_traceback}\n"
                f"An error occured while configuring the session.\n"
                f"The logs are availbe at {self.logs_path}"
            ) from None

        self._closed = False

    def _create_subprocess_and_java_api(
        self, distributed: bool, **kwargs: Any,
    ):
        py4j_java_port: Port
        if kwargs.get("use_remote_process", False):
            py4j_java_port = Port(_PY4J_DEFAULT_PORT)
            self._server_subprocess = None
            logging.getLogger("atoti.process").warning(
                "use_remote_process is True. Expecting a running server with Py4J listening on port %d",
                py4j_java_port,
            )
        else:
            self._server_subprocess = ServerSubprocess(
                port=Port(self._config.port) if self._config.port else None,
                url_pattern=self._config.url_pattern,
                max_memory=self._config.max_memory,
                java_args=self._config.java_args,
                extra_jars=self._config.extra_jars,
                **kwargs,
            )
            py4j_java_port = self._server_subprocess.py4j_java_port
        self._java_api: JavaApi = JavaApi(
            py4j_java_port=py4j_java_port, distributed=distributed
        )

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    @abstractmethod
    def cubes(self) -> _Cubes:
        """Cubes of the session."""

    @property
    def closed(self) -> bool:
        """Return whether the session is closed or not."""
        return self._closed

    @property
    def port(self) -> int:
        """Port on which the session is exposed.

        Can be set in :class:`~atoti.config.SessionConfiguration`.
        """
        return self._java_api.get_session_port()

    @property
    def url(self) -> str:
        """Public URL of the session.

        Can be set in :class:`~atoti.config.SessionConfiguration`.
        """
        return self._java_api.get_session_url()

    @property
    def excel_url(self) -> str:
        """URL of the Excel endpoint.

        To connect to the session in Excel, create a new connection to an Analysis Services.
        Use this URL for the `server` field and choose to connect with "User Name and Password":

        * Without authentication, leave these fields blank.
        * With Basic authentication, fill them with your username and password.
        * Other authentication types (such as Auth0) are not supported by Excel.
        """
        return f"{self.url}/xmla"

    @property
    def logs_path(self) -> Path:
        """Path to the session logs file."""
        if not self._server_subprocess:
            raise NotImplementedError(
                "The logs path is not available when using a query server process"
            )
        return self._server_subprocess.logs_path

    def logs_tail(self, n: int = 20) -> Logs:
        """Return the n last lines of the logs or all the lines if ``n <= 0``."""
        with open(self.logs_path) as logs:
            lines = logs.readlines()
            last_lines = lines[-n:] if n > 0 else lines
            # Wrap in a Logs to display nicely.
            return Logs(last_lines)

    def _configure_session(self):
        """Configure the session."""
        # Configure the plugins first
        for plugin in get_active_plugins():
            plugin.init_session(self)

        if self._config.branding:
            branding_directory = _create_branding_directory(self._config.branding)
            self._java_api.set_branding_directory(branding_directory)

        if self._config.metadata_db:
            self._java_api.set_metadata_db(
                _resolve_metadata_db(self._config.metadata_db)
            )

        if self._config.i18n_directory:
            if isinstance(self._config.i18n_directory, str):
                i18n_directory = Path(self._config.i18n_directory)
            else:
                i18n_directory = self._config.i18n_directory
            self._java_api.set_i18n_directory(str(i18n_directory.resolve().as_uri()))

        if self._config.default_locale:
            self._java_api.set_locale(self._config.default_locale)

        if self._config.roles is not None:
            self._java_api.configure_roles(self._config.roles)

        if self._config.https is not None:
            self._java_api.configure_https(self._config.https)

        if self._config.authentication is not None:
            # Show Pyright that same_site is not ``None`` in the lines below
            if not self._config.same_site:
                raise RuntimeError("same_site should be defined at this time")

            # The session ID is used to make the default basic authentication realm unique so that
            # multiple sessions running on the same machine can have different users and roles.
            #
            # We used to provide this uniqueness by suffixing the session port to the realm but we
            # cannot do this anymore because the session needs to be started to retrieve its port.
            #
            # We use the Py4J Java port instead since it is guaranteed to be unique
            # for each session running on a single machine too.
            session_id = str(
                self._server_subprocess.py4j_java_port
                if self._server_subprocess
                else _PY4J_DEFAULT_PORT
            )
            self._java_api.configure_authentication(
                self._config.authentication,
                self._config.same_site,
                self.name,
                session_id,
            )

        if (
            self._config.jwt_key_pair is not None
            and self._config.jwt_key_pair.public_key is not None
            and self._config.jwt_key_pair.private_key is not None
        ):
            self._java_api.set_jwt_key_pair(
                self._config.jwt_key_pair.public_key,
                self._config.jwt_key_pair.private_key,
            )

        # Other configuration
        self._additional_session_configuration()

        self._java_api.start_application()

    def _additional_session_configuration(self):
        """More specific actions to configure the session."""

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit this session's context manager.

        Close the session.

        """
        self.close()

    def _clear(self):
        """Clear this session and free all the associated resources."""
        self._java_api.clear_session()

    def close(self) -> None:
        """Close this session and free all the associated resources."""
        self._java_api.shutdown()
        if self._server_subprocess:
            self.wait()
        self._closed = True

    def wait(self) -> None:
        """Wait for the underlying server subprocess to terminate.

        This will prevent the Python process to exit.
        """
        if self._server_subprocess is None:
            raise ValueError("Server subprocess is not defined")
        self._server_subprocess.wait()

    def _refresh(self):
        """Refresh the session."""
        self._java_api.refresh(force_start=False)

    def _generate_token(self) -> str:
        """Return a token that can be used to authenticate against the server."""
        return self._java_api.generate_jwt()

    def _setup_app_form(
        self,
        name: str,
        action: str,
        *,
        inputs: Optional[
            Mapping[str, Mapping[str, Union[bool, float, int, str]]]
        ] = None,
    ):
        """Set up a form to be used in the app served by the session.

        Example::

            session._setup_app_form(
                "Add city",
                f"{session.url}/atoti/pyapi/{route}",
                inputs={
                    "City": {"placeholder": "Name of the city", "required": True},
                    "Value": {
                        "placeholder": "Value for the city",
                        "required": True,
                        "type": "number",
                    },
                },
            )

        Args:
            name: The name of the form.
            action: The URL at which the form will be submitted.
            inputs: Map of input name to properties to set in the corresponding ``<input />`` HTML element.
                Some of the accepted properties are listed `here <https://github.com/DefinitelyTyped/DefinitelyTyped/blob/ed541cd6d5f5e12bf6447163a1d53c767ae3cd87/types/react/index.d.ts#L2083 >`_.
        """
        self._java_api.setup_app_form(name, action, inputs or {})

    def _open_transient_query_session(self) -> QuerySession:
        from .query.auth import Auth
        from .query.session import QuerySession

        headers = self._generate_auth_headers()
        auth: Optional[Auth] = (lambda _url: headers) if headers else None
        return QuerySession(f"http://localhost:{self.port}", auth=auth, name=self.name)

    def _get_create_equivalent_widget_code(self) -> Optional[str]:
        if not run_from_ipython():
            return None

        session_variable_name = _find_corresponding_top_level_variable_name(self)
        if session_variable_name:
            return f"""{session_variable_name}.visualize()"""

        return f"""import atoti as tt\n\ntt.sessions["{self.name}"].visualize()"""

    @doc(_QUERY_MDX_DOC)
    def query_mdx(self, mdx: str, *, timeout: int = 30) -> QueryResult:
        query_result = self._open_transient_query_session().query_mdx(
            mdx,
            timeout=timeout,
            get_level_data_types=lambda cube_name, levels_coordinates: self.cubes[  # pylint: disable=protected-access
                cube_name
            ]._get_level_data_types(
                levels_coordinates
            ),
        )

        query_result._atoti_create_equivalent_widget_code = (  # pylint: disable=protected-access
            self._get_create_equivalent_widget_code()  # pylint: disable=protected-access
        )
        return query_result

    @doc(args=_QUERY_MDX_ARGS)
    def explain_mdx_query(self, mdx: str, *, timeout: int = 30) -> QueryAnalysis:
        """Explain an MDX query.

        {args}
        """
        return self._java_api.analyse_mdx(mdx, timeout)

    def _generate_auth_headers(self) -> Mapping[str, str]:
        """Generate the authentication headers to use for this session."""
        return {"Authorization": f"Jwt {self._java_api.generate_jwt()}"}

    def endpoint(
        self, route: str, *, method: Literal["POST", "GET", "PUT", "DELETE"] = "GET"
    ) -> Any:
        """Create a custom endpoint at ``f"{session.url}/atoti/pyapi/{route}"``.

        The decorated function must take three arguments with types :class:`~atoti.pyapi.user.User`, :class:`~atoti.pyapi.http_request.HttpRequest` and :class:`~atoti.session.Session` and return a response body as a Python data structure that can be converted to JSON.
        ``DELETE``, ``POST``, and ``PUT`` requests can have a body but it must be JSON.

        Path parameters can be configured by wrapping their name in curly braces in the route.

        Example::

            @session.endpoint("simple_get")
            def callback(request: HttpRequest, user: User, session: Session):
                return "something that will be in response.data"


            @session.endpoint(f"simple_post/{store_name}", method="POST")
            def callback(request: HttpRequest, user: User, session: Session):
                return request.path_parameters.store_name

        Args:
            route: The path suffix after ``/atoti/pyapi/``.
                For instance, if ``custom/search`` is passed, a request to ``/atoti/pyapi/custom/search?query=test#results`` will match.
                The route should not contain the query (``?``) or fragment (``#``).
            method: The HTTP method the request must be using to trigger this endpoint.
        """
        if route[0] == "/" or "?" in route or "#" in route:
            raise ValueError(
                f"Invalid route '{route}'. It should not start with '/' and not contain '?' or '#'."
            )

        def endpoint_decorator(func: CallbackEndpoint) -> Callable:
            self._java_api.create_endpoint(
                route, PyApiEndpoint(func, self), method, self.url,
            )
            return func

        return endpoint_decorator

    def export_translations_template(self, path: Union[Path, str]):
        """Export a template containing all translatable values in the session's cubes.

        Args:
            path: The path at which to write the template.
        """
        self._java_api.export_i18n_template(path)

    def visualize(  # pylint: disable=no-self-use
        self, *args: Any, **kwargs: Any
    ) -> None:
        """atoti-jupyterlab is required."""
        raise MissingPluginError("jupyterlab")

    def _repr_html(self) -> str:
        return convert_repr_json_to_html(self)

    @abstractmethod
    def _repr_json_(self) -> ReprJson:
        ...
