# -*- coding: utf-8 -*-

"""Get all active enterprises and save to json file for later use."""
import json
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.result import ResultE, safe
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class CacheEnterprises(object):
    """Get all enterprises and write them to a json file."""

    _get_all_enterprises: Callable[[], ResultE[dict]]
    _write: Callable

    def __call__(self) -> ResultE[bool]:
        """Call api get list and write to file."""
        return self._get_all_enterprises(
        ).bind(
            safe(json.dumps),  # safe wraps impure call
        ).bind(
            partial(self._write, file_path='cache.json'),
        )
