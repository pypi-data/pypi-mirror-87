import os
from typing import Any, Dict

from attr import dataclass
from returns.maybe import Maybe
from returns.result import safe
from typing_extensions import final

from p360_contact_manager.constants import Argument


@final
@dataclass(frozen=True, slots=True)
class ParseEnvironmentVariables(object):
    """Parses Environment variables meant for p360 into a dict."""

    @safe
    def __call__(self) -> dict:
        """Gather arguments."""
        arguments: Dict[str, Any] = {}

        for arg in Argument:
            self._get_variable(arg).map(arguments.update)

        return arguments

    def _get_variable(self, arg: Argument) -> Maybe[dict]:
        return Maybe.from_value(
            os.environ.get(arg.as_env()),
        ).map(
            lambda env_val: {arg.name: env_val},
        )
