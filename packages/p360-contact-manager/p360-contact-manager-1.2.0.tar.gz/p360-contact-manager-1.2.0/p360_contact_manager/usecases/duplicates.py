import json
import logging
from copy import deepcopy
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe
from typing_extensions import Final, final

RECNO: Final[str] = 'Recno'
UPDATE: Final[str] = 'update'
SKIP: Final[str] = 'skip'


@final
@dataclass(frozen=True, slots=True)
class Duplicates(object):
    """Produce worklist that contains entries which has duplicates in p360."""

    _get_all_enterprises: Callable
    _write: Callable

    _output: str = 'duplicate_worklist.json'
    _duplicate_remove_payload: dict = {
        'Recno': None,
        'Active': False,
        'EnterpriseNumber': '',
    }
    _log = logging.getLogger('produce_list')

    def __call__(self) -> ResultE[bool]:
        """Load enterprises, remove duplicates, restructure, write worklist."""
        return flow(
            self._get_all_enterprises(),
            bind(self._group_by_org_no),
            bind(self._remove_non_duplicates),
            bind(self._restructure_data),
            bind(self._restructure_with_payload),
            bind(safe(json.dumps)),
            bind(partial(self._write, file_path=self._output)),
        )

    @safe
    def _group_by_org_no(self, payload) -> dict:

        grouped: dict = {}
        for enterprise in payload.get('Enterprises'):
            e_number = enterprise.get('EnterpriseNumber')
            # any enterprise without a number we will skip
            if not e_number:
                continue

            # any enterprise with 'recno:1' in categories are internal and
            # should be skipped
            if 'recno:1' in enterprise.get('Categories', []):
                continue

            if e_number not in grouped:
                grouped[e_number] = []

            grouped[e_number].append(enterprise)

        return grouped

    @safe
    def _remove_non_duplicates(self, payload) -> dict:

        for org_no in list(payload.keys()):
            if len(payload[org_no]) == 1:
                payload.pop(org_no)

        return payload

    @safe
    def _restructure_data(self, org_dict: dict) -> dict:
        restructured: dict = {UPDATE: [], SKIP: []}
        for orgno in org_dict:  # noqa: WPS528
            temp = self._restructure_with_skip(org_dict[orgno])
            if is_successful(temp):
                restructured[UPDATE].extend(temp.unwrap().get(UPDATE))
                restructured[SKIP].append(temp.unwrap().get(SKIP))
            else:
                self._log.warning('Unable to restructure data:')
                self._log.warning(org_dict[orgno])
        return restructured

    @safe
    def _restructure_with_skip(self, organizations: list) -> dict:
        restructured: dict = {}
        min_recno = organizations[0][RECNO]
        index = 0

        for list_index, org in enumerate(organizations):
            if org[RECNO] < min_recno:
                min_recno = org[RECNO]
                index = list_index

        restructured[SKIP] = organizations.pop(index)
        restructured[UPDATE] = organizations
        return restructured

    @safe
    def _restructure_with_payload(self, enterprises: dict) -> dict:

        update_list = []

        for enterprise in enterprises[UPDATE]:
            payload = deepcopy(self._duplicate_remove_payload)
            payload[RECNO] = enterprise[RECNO]
            update_list.append({
                'original_data': enterprise,
                'payload': {'parameter': payload},
            })

        enterprises[UPDATE] = update_list
        return enterprises
