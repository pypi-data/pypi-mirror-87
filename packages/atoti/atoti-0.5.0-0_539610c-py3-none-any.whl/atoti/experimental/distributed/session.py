from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..._local_session import ALocalSession
from ..._repr_utils import repr_json_session
from ...config import SessionConfiguration
from .cube import DistributedCube
from .cubes import DistributedCubes

if TYPE_CHECKING:
    from ..._repr_utils import ReprJson


class DistributedSession(ALocalSession):
    """Holds a connection to the Java gateway."""

    def __init__(
        self, name: str, *, config: SessionConfiguration, **kwargs: Any,
    ):
        """Create the session and the Java gateway.

        Args:
            name: The name of the session.
            config: The configuration of the session.

        """
        super().__init__(name, config, True, **kwargs)
        self._cubes = DistributedCubes(self._java_api)

    def __enter__(self) -> DistributedSession:
        """Enter this session's context manager.

        Returns:
            self: to assign it to the "as" keyword.

        """
        return self

    @property
    def cubes(self) -> DistributedCubes:
        """Cubes of the session."""
        return self._cubes

    def create_cube(self, name: str) -> DistributedCube:
        """Create a distributed cube.

        Args:
            name: The name of the created cube.
        """
        self._java_api.create_distributed_cube(name)
        self._java_api.refresh(force_start=True, check_errors=False)
        self.cubes[name] = DistributedCube(self._java_api, name, self)

        return self.cubes[name]

    def _repr_json_(self) -> ReprJson:
        return repr_json_session(self)
