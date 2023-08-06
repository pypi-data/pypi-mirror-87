# -*- coding: utf-8 -*-

"""Update data with p360 through UpdateEnterprise api endpoint."""
import json
import logging
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe
from typing_extensions import Final, final

RECNO: Final = 'Recno'


@final
@dataclass(frozen=True, slots=True)
class Update(object):
    """Update worklist data with p360."""

    _worklist: str
    _error_margin: int

    _update_enterprise: Callable
    _read: Callable
    _write: Callable

    _output: str = 'result_update.json'
    _log = logging.getLogger('usecases.Update')

    def __call__(self) -> ResultE[bool]:
        """Read worklist, update to p360, write result file."""
        return flow(
            self._read(self._worklist, 'r'),
            bind(safe(json.loads)),
            bind(self._get_update_list),
            bind(self._handle_worklist),
            bind(safe(json.dumps)),
            bind(partial(self._write, file_path=self._output)),
        )

    @safe
    def _get_update_list(self, input_data: dict) -> list:
        return input_data['update']

    @safe
    def _handle_worklist(self, worklist: list) -> dict:

        # loop enterprises
        # call update endpoint
        # if okay, put to okay,
        # if bad, put to bad with error_message
        # continue
        update_result: dict = {
            'errors': 0,
            'updated': [],
            'failed': [],
        }
        for ent in worklist:
            ent_no = ent['original_data']['EnterpriseNumber']
            recno = ent['original_data']['Recno']
            self._log.info('Current enterprise: %s, recno: %s', ent_no, recno)

            update = self._update_enterprise(ent['payload'])
            self._log.info(update)

            if is_successful(update):
                update_result['updated'].append(recno)
                continue

            update_result['errors'] += 1
            update_result['failed'].append(
                {
                    'recno': recno,
                    'enterprise_number': ent_no,
                    'payload': ent['payload'],
                    'error_message': str(update.failure()),
                },
            )

            if update_result['errors'] > self._error_margin:
                self._log.error('Exceeded error margin, stopping execution')
                return update_result

        return update_result
