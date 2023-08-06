import json
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.functions import tap
from returns.pipeline import flow
from returns.pointfree import bind, map_, rescue
from returns.result import ResultE, safe
from typing_extensions import final

from p360_contact_manager.common import ReadLocalFile, WriteLocalFile


@final
@dataclass(frozen=True, slots=True)
class LoadSettings(object):
    """Loads application settings from json file."""

    filename: str = 'settings.json'
    _read_file: Callable = ReadLocalFile()
    _write_file: Callable = WriteLocalFile()

    def __call__(self) -> ResultE[dict]:
        """Run load settings flow."""
        return flow(
            self.filename,
            partial(self._read_file, mode='r'),
            bind(safe(json.loads)),
            rescue(safe(lambda _: {})),
        )


@final
@dataclass(frozen=True, slots=True)
class StoreSettings(object):
    """Update settings file with values from dict param."""

    filename: str = 'settings.json'
    _read: Callable = ReadLocalFile()
    _write: Callable = WriteLocalFile()

    def __call__(self, settings: dict) -> ResultE[bool]:
        """Run store settings flow."""
        return flow(
            self.filename,
            partial(self._read, mode='r'),
            bind(safe(json.loads)),
            # old.update returns none, so tap it to return `old`
            map_(tap(lambda old: old.update(settings))),  # type: ignore
            bind(safe(json.dumps)),
            bind(partial(self._write, file_path=self.filename)),
        )
