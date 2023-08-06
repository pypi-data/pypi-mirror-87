# -*- coding: utf-8 -*-

"""Code to produce a list of organizations from ContactService api."""
import json
import logging
from copy import deepcopy
from typing import Callable

import requests
from attr import dataclass
from returns.functions import raise_exception
from returns.pipeline import is_successful
from returns.result import ResultE, Success, safe
from typing_extensions import Final, final

URL_PARAM_AUTHKEY: Final[str] = 'authkey'


@final
@dataclass(frozen=True, slots=True)
class Ping(object):
    """Ping p360 endpoint."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'Ping'

    def __call__(
        self,
        timeout: int = 10,
    ) -> ResultE[requests.Response]:
        """Call api get list and write to file."""
        if self._dry:
            return Success('DRY RUN: No API calls executed')  # type: ignore

        return self._post(
            self._p360_base_url + self._endpoint,
            url_params={'authkey': self._authkey},
            payload={},
            timeout=timeout,
        )


@final
@dataclass(frozen=True, slots=True)
class UpdateEnterprise(object):
    """Produce a list of Organizations."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'UpdateEnterprise'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 10,
    ) -> requests.Response:
        """Call api get list and write to file."""
        if self._dry:
            return 'DRY RUN: No API calls executed'  # type: ignore

        response = self._post(
            self._p360_base_url + self._endpoint,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            payload=payload,
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        response_json = response.unwrap().json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        return response_json


@final
@dataclass(frozen=True, slots=True)
class SynchronizeEnterprise(object):
    """Produce a list of Organizations."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _dry: bool = False
    _endpoint = 'SynchronizeEnterprise'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 20,
    ) -> requests.Response:
        """Call api syncronize endpoint with given payload."""
        if self._dry:
            return 'DRY RUN: No API calls executed'  # type: ignore

        response = self._post(
            self._p360_base_url + self._endpoint,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            payload=payload,
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        response_json = response.unwrap().json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        return response_json


@final
@dataclass(frozen=True, slots=True)
class GetEnterprises(object):
    """Call get enterprises endpoint with given payload."""

    _authkey: str
    _p360_base_url: str
    _post: Callable

    _endpoint = 'GetEnterprises'

    @safe
    def __call__(
        self,
        payload: str,
        timeout: int = 20,
    ) -> requests.Response:
        """Call api get list and write to file."""
        response = self._post(
            self._p360_base_url + self._endpoint,
            payload=payload,
            url_params={URL_PARAM_AUTHKEY: self._authkey},
            timeout=timeout,
        )

        if not is_successful(response):
            raise response.failure()

        resp = response.unwrap()
        content_type = resp.headers.get('Content-Type')
        if not content_type or 'application/json' not in content_type:
            raise RuntimeError(
                'Content-type "{type}" is not equal to application/json'.format(
                    type=content_type,
                ),
            )

        response_json = resp.json()

        if not response_json.get('Successful'):
            raise RuntimeError(response_json['ErrorMessage'])

        if not response_json.get('Enterprises'):
            raise ValueError('No enterprises found')

        return response_json


@final
@dataclass(frozen=True, slots=True)
class GetAllEnterprises(object):
    """Call p360 api and return all enterprises."""

    _get_enterprises: Callable
    _p360_search_criteria: dict = {
        'parameter': {
            'Active': True,
            'Page': 0,
            'MaxRows': 20,
            'SortCriterion': 'RecnoDescending',
            'IncludeCustomFields': False,
        },
    }
    _log = logging.getLogger('api.p360.GetAllEnterprises')

    @safe
    def __call__(self) -> dict:
        """Use payload and get all enterprises."""
        payload = deepcopy(self._p360_search_criteria)

        aggregated = self._get_enterprises(payload).alt(
            raise_exception,
        ).unwrap()
        # create reference to enterprises array in first request

        for page in range(1, aggregated['TotalPageCount']):
            payload['parameter']['Page'] = page

            self._log.info(
                'Processing {page} page out of {pages} pages'.format(
                    page=page,
                    pages=aggregated['TotalPageCount'],
                ),
            )

            self._call_api(payload).map(
                # Add to enterprises list in aggregated result.
                aggregated['Enterprises'].extend,
            )

        return aggregated

    def _call_api(self, payload) -> ResultE[list]:
        return self._get_enterprises(payload).map(
            lambda response: response.get('Enterprises'),
        )


@final
@dataclass(frozen=True, slots=True)
class GetAllCachedEnterprises(object):
    """Get return contents of cache.json if exists."""

    _read: Callable
    _cache_file: str

    def __call__(self) -> ResultE[dict]:
        """Read data load to json and return."""
        return self._read(self._cache_file, 'r').map(
            json.loads,
        )
