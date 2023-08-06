from enum import Enum

from typing_extensions import Final

ENV_PREFIX: Final[str] = 'P360'


class Argument(Enum):
    """Helper dataclass for our arguments."""

    authkey: Final[str] = 'authkey'
    output: Final[str] = 'output'
    worklist: Final[str] = 'worklist'
    p360_base_url: Final[str] = 'p360_base_url'
    brreg_base_url: Final[str] = 'brreg_base_url'
    kommune_numbers: Final[str] = 'kommune_numbers'
    cached: Final[str] = 'cached'
    dry: Final[str] = 'dry'
    error_margin: Final[str] = 'error_margin'

    def as_cmd_arg(self) -> str:
        """Get argument with double dashes."""
        return '--{name}'.format(name=self.name)

    def as_env(self) -> str:
        """Get argument as a capitalized env var."""
        return '{prefix}_{name}'.format(
            prefix=ENV_PREFIX,
            name=self.name.upper(),
        )
