# -*- coding: utf-8 -*-

"""Synchronize data with p360 through SynchronizeEnterprise api endpoint."""
import json
import logging
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class Synchronize(object):
    """Synchronize worklist data with p360."""

    _worklist: str
    _error_margin: int

    _synchronize_enterprise: Callable
    _read: Callable
    _write: Callable

    _output: str = 'result_synchronize.json'
    _log = logging.getLogger('usecases.Synchronize')

    def __call__(self) -> ResultE[bool]:
        """Read worklist, synchronize to p360, write result file."""
        return flow(
            self._read(self._worklist, 'r'),
            bind(safe(json.loads)),
            bind(self._handle_worklist),
            bind(safe(json.dumps)),
            bind(partial(self._write, file_path=self._output)),
        )

    @safe
    def _handle_worklist(self, worklist: list) -> dict:
        """Handle the input worklist file.

        Loop enterprises
        call synchronize endpoint
        if okay, put to okay,
        if bad, put to bad with error_message
        continue
        """
        sync_result: dict = {
            'errors': 0,
            'synchronized': [],
            'failed': [],
        }
        for ent in worklist:
            payload = ent['payload']
            ent_no = payload['parameter']['EnterpriseNumber']
            self._log.info('Current enterprise: %s', ent_no)
            self._log.info('brreg url: %s', ent['brreg_url'])

            sync = self._synchronize_enterprise(payload)
            self._log.info(sync)

            if is_successful(sync):
                sync_result['synchronized'].append(ent_no)
                continue

            sync_result['errors'] += 1
            sync_result['failed'].append(
                {
                    'enterprise_number': ent_no,
                    'payload': payload,
                    'error_message': str(sync.failure()),
                },
            )

            if sync_result['errors'] > self._error_margin:
                self._log.error('Exceeded error margin, stopping execution')
                return sync_result

        return sync_result
