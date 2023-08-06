from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, Mapping, Optional, Type, TypeVar, Union

from typing_extensions import Literal

from ..sampling import DEFAULT_SAMPLING_MODE, SamplingMode
from ._auth import Auth
from ._auth_utils import parse_auth
from ._branding import Branding
from ._https import HttpsConfiguration
from ._jwt import JwtKeyPair
from ._role import Role
from ._utils import Configuration, defined_kwargs

DEFAULT_URL_PATTERN = "{protocol}://localhost:{port}"

SameSiteCookie = Literal["lax", "none", "strict"]

_T = TypeVar("_T")


def _get_or_fallback(main: _T, fallback: _T) -> _T:
    return main if main is not None else fallback


SubConfig = TypeVar("SubConfig", bound=Configuration)


def _pop_subconfig(
    field: str, config: Type[SubConfig], data: Dict[str, Any]
) -> Optional[SubConfig]:
    return config._from_dict(data.pop(field)) if field in data else None


@dataclass(frozen=True)
class SessionConfiguration(Configuration):
    """Configuration of the session."""

    authentication: Optional[Auth]
    branding: Optional[Branding]
    cache_cloud_files: Optional[bool]
    default_locale: Optional[str]
    extra_jars: Optional[Collection[str]]
    https: Optional[HttpsConfiguration]
    i18n_directory: Optional[Union[Path, str]]
    inherit_global_config: bool
    java_args: Optional[Collection[str]]
    jwt_key_pair: Optional[JwtKeyPair]
    max_memory: Optional[str]
    metadata_db: Optional[str]
    port: Optional[int]
    roles: Optional[Collection[Role]]
    same_site: Optional[SameSiteCookie]
    sampling_mode: Optional[SamplingMode]
    url_pattern: Optional[str]

    @classmethod
    def _create(cls, data: Mapping[str, Any]):
        # Convert mapping to a dict to make it mutable with a pop method
        data_dict: Dict[str, Any] = dict(data)
        auth = (
            parse_auth(data_dict.pop("authentication"))
            if "authentication" in data_dict
            else None
        )

        branding = _pop_subconfig("branding", Branding, data_dict)
        https = _pop_subconfig("https", HttpsConfiguration, data_dict)

        i18n_directory = data_dict.pop("i18n_directory", None)
        if i18n_directory is not None:
            i18n_directory = Path(i18n_directory)

        jwt_key_pair = _pop_subconfig("jwt_key_pair", JwtKeyPair, data_dict)

        roles = (
            [Role._from_dict(role) for role in data_dict.pop("roles")]
            if "roles" in data_dict
            else None
        )

        sampling_mode = _pop_subconfig("sampling_mode", SamplingMode, data_dict)

        return create_config(
            **defined_kwargs(
                authentication=auth,
                branding=branding,
                https=https,
                i18n_directory=i18n_directory,
                jwt_key_pair=jwt_key_pair,
                roles=roles,
                sampling_mode=sampling_mode,
                **data_dict,
            ),
        )

    def _validate_before_completion(self):
        """Validate the merged config before applying the remaining default values."""
        if self.same_site:
            if not self.authentication:
                raise ValueError(
                    "same_site was needlessly configured since authentication is not set up"
                )

            if self.same_site == "none" and not (
                self.url_pattern and self.url_pattern.startswith("https://")
            ):
                raise ValueError(
                    "same_site was set to none which requires url_pattern to start with https://"
                )

    def _complete_with_default(self) -> SessionConfiguration:
        """Copy the config into a new one with the default values.

        These values should only be set if ``None`` is provided.
        They are not set when creating the configuration to able clean merging.
        """
        self._validate_before_completion()

        return SessionConfiguration(
            authentication=self.authentication,
            branding=self.branding,
            cache_cloud_files=_get_or_fallback(self.cache_cloud_files, True),
            inherit_global_config=self.inherit_global_config,
            default_locale=self.default_locale,
            extra_jars=self.extra_jars,
            https=self.https,
            i18n_directory=self.i18n_directory,
            java_args=self.java_args,
            jwt_key_pair=self.jwt_key_pair,
            max_memory=self.max_memory,
            metadata_db=self.metadata_db,
            port=self.port,
            roles=self.roles,
            same_site=_get_or_fallback(self.same_site, "lax"),
            sampling_mode=_get_or_fallback(self.sampling_mode, DEFAULT_SAMPLING_MODE),
            url_pattern=_get_or_fallback(self.url_pattern, DEFAULT_URL_PATTERN),
        )


def merge_config(
    instance1: Optional[SessionConfiguration],
    instance2: Optional[SessionConfiguration],
) -> SessionConfiguration:
    """Merge two configurations. Second overrides the first one."""
    if instance1 is None:
        if instance2 is None:
            return create_config()
        return instance2
    if instance2 is None:
        return instance1
    return SessionConfiguration(
        authentication=_get_or_fallback(
            instance2.authentication, instance1.authentication
        ),
        branding=_get_or_fallback(instance2.branding, instance1.branding),
        cache_cloud_files=_get_or_fallback(
            instance2.cache_cloud_files, instance1.cache_cloud_files
        ),
        default_locale=_get_or_fallback(
            instance2.default_locale, instance1.default_locale
        ),
        extra_jars=_get_or_fallback(instance2.extra_jars, instance1.extra_jars),
        https=_get_or_fallback(instance2.https, instance1.https),
        i18n_directory=_get_or_fallback(
            instance2.i18n_directory, instance1.i18n_directory
        ),
        inherit_global_config=instance2.inherit_global_config,
        java_args=_get_or_fallback(instance2.java_args, instance1.java_args),
        jwt_key_pair=_get_or_fallback(instance2.jwt_key_pair, instance1.jwt_key_pair),
        max_memory=_get_or_fallback(instance2.max_memory, instance1.max_memory),
        metadata_db=_get_or_fallback(instance2.metadata_db, instance1.metadata_db),
        port=_get_or_fallback(instance2.port, instance1.port),
        roles=_get_or_fallback(instance2.roles, instance1.roles),
        same_site=_get_or_fallback(instance2.same_site, instance1.same_site),
        sampling_mode=_get_or_fallback(
            instance2.sampling_mode, instance1.sampling_mode
        ),
        url_pattern=_get_or_fallback(instance2.url_pattern, instance1.url_pattern),
    )


def create_config(
    *,
    authentication: Optional[Auth] = None,
    branding: Optional[Branding] = None,
    cache_cloud_files: Optional[bool] = None,
    default_locale: Optional[str] = None,
    extra_jars: Optional[Collection[Union[str, Path]]] = None,
    https: Optional[HttpsConfiguration] = None,
    i18n_directory: Optional[Union[Path, str]] = None,
    inherit_global_config: bool = True,
    java_args: Optional[Collection[str]] = None,
    jwt_key_pair: Optional[JwtKeyPair] = None,
    max_memory: Optional[str] = None,
    metadata_db: Optional[Union[Path, str]] = None,
    port: Optional[int] = None,
    roles: Optional[Collection[Role]] = None,
    same_site: Optional[SameSiteCookie] = None,
    sampling_mode: Optional[SamplingMode] = None,
    url_pattern: Optional[str] = None,
) -> SessionConfiguration:
    """Create a configuration.

    Note:
        Configuration inheritance is enabled by default.
        Pass ``inherit_global_config=False`` to prevent this configuration from being merged with the global one.

    Args:
        authentication: The authentication mechanism that will be used by the server.
        branding: The UI elements to change in the app to replace the atoti branding with another one.
        cache_cloud_files: Whether to cache loaded cloud files locally in the temp directory.
            Watched files will not be cached.
            Defaults to ``True``.
        default_locale: The default locale to use for internationalizing the session.
        extra_jars: A collection of JAR paths that will be added to the classpath of the Java process.
        https: The certificate and its password used to enable HTTPS on the application.
        i18n_directory: The directory from which translation files will be loaded.
            It should contain a list of files named after their corresponding locale (e.g. ``en-US.json`` for US translations).
            The application will behave differently depending on how ``metadata_db`` is configured:

            * If ``metadata_db`` is a path to a file:

              - If a value is specified for ``i18n_directory``, those files will be uploaded to the local metadata DB, overriding any previously defined translations.
              - If no value is specified for ``i18n_directory``, the default translations for atoti will be uploaded to the local metadata DB.

            * If a remote metadata DB has been configured:

              - If a value is specified for ``i18n_directory``, this data will be pushed to the remote metadata DB, overriding any previously existing values.
              - If no value has been specified for ``i18n_directory`` and translations exist in the remote metadata DB, those values will be loaded into the session.
              - If no value has been specified for ``i18n_directory`` and no translations exist in the remote  metadata DB, the default translations for atoti will be uploaded to the remote  metadata DB.
        inherit_global_config: Whether this config should be merged with the default config if it exists.
            The path of the default config is ``$ATOTI_HOME/config.yml`` where the ``$ATOTI_HOME`` environment variable defaults to ``$HOME/.atoti``.
        java_args: Collection of additional arguments to pass to the Java process.
            For instance: ``["-verbose:gc", "-Xms1g", "-XX:+UseG1GC"]``.
        jwt_key_pair: The key pair to use for signing :abbr:`JWT (JSON Web Token)` s.
        max_memory: Max memory allocated to each session.
            Actually sets the ``-Xmx`` JVM parameter.
            The format is a string containing a number followed by a unit among ``G``, ``M`` and ``K``.
            For instance: ``64G``.
            Defaults to the JVM default memory which is 25% of the machine memory.
        metadata_db: The description of the database where the session's metadata will be stored.
            If a path to a file is given, it will be created if needed.
        port: The port on which the session will be exposed.
            Defaults to a random available port.
        roles: The roles and their restrictions.
            There are 2 predefined roles in atoti:

              - ``ROLE_USER``: required to access the application
              - ``ROLE_ADMIN``: gives full access (read, write, delete, etc...) to the application
        same_site: The value to use for the `SameSite <https://web.dev/samesite-cookies-explained/>`_ attribute of the HTTP cookie sent by the session when ``authentication`` is configured.
            Setting it to ``none`` requires the session to be served in HTTPS so ``url_pattern`` must also be defined and start with ``https://``.
            Defaults to ``lax``.
        sampling_mode: The sampling mode describing how files are loaded into the stores.
            It is faster to build the data model when only part of the data is loaded.

            Modes are available in :mod:`atoti.sampling`.

            If not :data:`~atoti.sampling.FULL`, call :meth:`~atoti.session.Session.load_all_data` to load everything once the model definition is done.
        url_pattern: The pattern used to build the URL accessed through :attr:`atoti.session.Session.url`.
            The following placeholder replacements will be made:

                * ``{host}``: The address of the machine hosting the session.
                * ``{port}``: The port on which the session is exposed.
                * ``{protocol}``: ``http`` or ``https`` depending on whether the ``https`` option was defined or not.

            Defaults to ``{protocol}://localhost:{port}``.
    """
    return SessionConfiguration(
        authentication=authentication,
        branding=branding,
        cache_cloud_files=cache_cloud_files,
        default_locale=default_locale,
        extra_jars=[
            str(jar.absolute()) if isinstance(jar, Path) else jar for jar in extra_jars
        ]
        if extra_jars
        else None,
        https=https,
        i18n_directory=i18n_directory,
        inherit_global_config=inherit_global_config,
        java_args=java_args,
        jwt_key_pair=jwt_key_pair,
        max_memory=max_memory,
        metadata_db=str(metadata_db.absolute())
        if isinstance(metadata_db, Path)
        else metadata_db,
        port=port,
        roles=roles,
        same_site=same_site,
        sampling_mode=sampling_mode,
        url_pattern=url_pattern,
    )
