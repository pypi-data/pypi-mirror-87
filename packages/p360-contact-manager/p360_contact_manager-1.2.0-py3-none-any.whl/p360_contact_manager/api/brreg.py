import logging
from typing import Callable

import requests
from attr import dataclass
from returns.functions import tap
from returns.pipeline import flow
from returns.pointfree import alt, bind, rescue
from returns.result import ResultE, safe
from typing_extensions import final


@final
@dataclass(frozen=True, slots=True)
class GetOrganization(object):
    """Produce a list of Organizations."""

    _brreg_base_url: str
    _get: Callable[[str], ResultE[requests.Response]]

    _entities = 'enheter/'
    _sub_entities = 'underenheter/'

    def __call__(
        self,
        organization_number: str,
    ) -> ResultE[dict]:
        """Call api get list and write to file."""
        return flow(
            # URL param
            self._brreg_base_url + self._entities + organization_number,
            # Request data (io)
            self._get,
            # on failure retry with _sub_entities
            rescue(  # type: ignore
                lambda _: self._get(
                    self._brreg_base_url
                    + self._sub_entities  # noqa: W503
                    + organization_number,  # noqa: W503
                ),
            ),
            # return json data
            bind(self._get_json),
        )

    @safe
    def _get_json(self, response: requests.Response) -> dict:
        return response.json()


@final
@dataclass(frozen=True, slots=True)
class GetOrganizations(object):
    """Get a list of organizations with the given criteria."""

    _brreg_base_url: str
    _get: Callable

    _entities = 'enheter/'
    _sub_entities = 'underenheter/'

    _log = logging.getLogger('api.brreg.GetOrganizations')

    def __call__(
        self,
        search_criteria: dict,
        timeout: int = 20,
    ) -> ResultE[list]:
        """Call api with the search criteria and and return list."""
        return flow(
            # Get data from brreg
            self._get(
                self._brreg_base_url + self._entities,
                url_params=search_criteria,
                timeout=timeout,
            ),
            # log on error
            alt(tap(self._log.warning)),
            # return json data
            bind(self._get_json),
        )

    @safe
    def _get_json(self, response: requests.Response) -> list:
        return response.json()


@final
@dataclass(frozen=True, slots=True)
class GetAllOrganizations(object):
    """Get an accumulated list of organizations with the given criteria."""

    _get_organizations: Callable

    _log = logging.getLogger('api.brreg.GetAllOrganizations')
    _brreg_max_enterprises: int = 10000

    @safe
    def __call__(
        self,
        search_criteria: dict,
        timeout: int = 20,
    ) -> list:
        """Call api with the search criteria and and return list."""
        business_types = search_criteria['naeringskode'].split(',')
        kommune_numbers = search_criteria['kommunenummer'].split(',')
        search_criteria['naeringskode'] = business_types[0]

        all_orgs: list = []

        for kommune_number in kommune_numbers:
            for business_type in business_types:
                search_criteria['page'] = 0
                search_criteria['naeringskode'] = business_type
                search_criteria['kommunenummer'] = kommune_number

                self._log.info(
                    'Current search criteria %s', search_criteria,
                )

                self._paginator(search_criteria).map(
                    all_orgs.extend,
                ).alt(
                    tap(print),
                )

        return all_orgs

    @safe
    def _paginator(self, search_criteria) -> list:
        aggregated_data = self._get_organizations(search_criteria).unwrap()
        page = aggregated_data.get('page')
        total_elements = page.get('totalElements')
        self._log.info(
            '%s elements in %s pages',
            page.get('totalElements'),
            page.get('totalPages'),
        )

        if total_elements < 1:
            return []

        if total_elements > self._brreg_max_enterprises:
            error = 'Number of results exceedes 10 000'
            raise RuntimeError(error)

        for page_number in range(1, page.get('totalPages')):
            search_criteria['page'] = page_number

            self._call_api(search_criteria).map(
                aggregated_data['_embedded']['enheter'].extend,
            ).alt(
                tap(self._log.warning),
            )

        return aggregated_data['_embedded']['enheter']

    def _call_api(self, search_criteria) -> ResultE[list]:
        return flow(
            # search payload
            search_criteria,
            # get organizations (IO)
            self._get_organizations,
            # return list of organizations in `enheter`
            bind(safe(lambda resp: resp.get('_embedded').get('enheter'))),
            # log warning on failure
            alt(tap(self._log.warning)),
        )
