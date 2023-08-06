import json
import logging
from typing import Callable

from attr import dataclass
from returns.curry import partial
from returns.maybe import Maybe
from returns.pipeline import flow, is_successful
from returns.pointfree import bind
from returns.result import ResultE, safe
from typing_extensions import Final, final

RECNO: Final = 'Recno'


@final
@dataclass(frozen=True, slots=True)
class BrregSyncronize(object):
    """Find Enterprises in brreg and create 'create' worklist for p360."""

    _kommune_numbers: str

    _get_all_organizations: Callable
    _write: Callable
    _get_country: Callable

    _output: str = 'worklist_brreg_synchronize.json'
    _brreg_search_criteria: dict = {}
    _log = logging.getLogger('usecases.BrregSyncronize')

    def __call__(self) -> ResultE[bool]:
        """Call api get list and write to file."""
        self._brreg_search_criteria['kommunenummer'] = self._kommune_numbers

        return flow(
            self._brreg_search_criteria,
            self._get_all_organizations,
            bind(self._create_worklist),
            bind(safe(json.dumps)),  # safe wrap impure json.dumps
            bind(partial(self._write, file_path=self._output)),
        )

    @safe
    def _create_worklist(self, brreg_list: list) -> list:
        self._log.info('Number of entities %s', len(brreg_list))
        worklist = []

        for entity in brreg_list:
            p360_payload = self._map_brreg_data_to_p360(entity)
            brreg_url = entity['_links']['self']['href']
            if is_successful(p360_payload):
                worklist.append(
                    {
                        'brreg_url': brreg_url,
                        # 'brreg_data': entity,  # noqa: E800
                        'payload': p360_payload.unwrap(),
                    },
                )
                continue

            self._log.warning(p360_payload.failure())
            self._log.warning(entity)

        return worklist

    @safe
    def _map_brreg_data_to_p360(
        self, brreg_data: dict,
    ) -> dict:

        p360_payload: dict = {
            'EnterpriseNumber': brreg_data['organisasjonsnummer'],
        }

        if brreg_data.get('slettedato') and brreg_data['slettedato']:
            raise RuntimeError(
                'The Organization is Deleted: {0}'.format(
                    brreg_data['slettedato'],
                ),
            )

        Maybe.from_value(brreg_data.get('navn')).map(
            lambda name: p360_payload.update({'Name': name}),
        )
        Maybe.from_value(brreg_data.get('hjemmeside')).map(
            lambda web: p360_payload.update({'Web': web}),
        )

        office = brreg_data.get('forretningsadresse')
        if office:
            country = self._get_country(office.get('landkode'))
            if not is_successful(country):
                raise country.failure()

            p360_payload.update({
                'OfficeAddress': {
                    'Country': country.unwrap().alpha3,
                    'County': office['kommune'],
                    'StreetAddress': ', '.join(office['adresse']),
                    'ZipCode': office['postnummer'],
                    'ZipPlace': office['poststed'],
                },
            })

        post = brreg_data.get('postadresse')
        if post:
            country = self._get_country(post.get('landkode'))
            if not is_successful(country):
                raise country.failure()

            Maybe.from_value(post.get('kommune')).map(
                lambda web: p360_payload.update({'Web': web}),
            )

            p360_payload.update({
                'PostAddress': {
                    'Country': country.unwrap().alpha3,
                    'County': post.get('kommune'),  # only for norway
                    'StreetAddress': ', '.join(post['adresse']),
                    'ZipCode': post.get('postnummer'),
                    'ZipPlace': post.get('poststed'),
                },
            })
        elif office:
            p360_payload.update(
                {'PostAddress': p360_payload.get('OfficeAddress')},
            )

        return {'parameter': p360_payload}
