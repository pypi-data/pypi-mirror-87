# -*- coding: utf-8 -*-

"""Common functions for contactservice package."""

import logging
from typing import Any, Optional, overload

import requests
from attr import dataclass
from iso3166 import countries
from returns.pipeline import flow
from returns.pointfree import alt
from returns.result import ResultE, safe
from typing_extensions import Literal, final


@final
@dataclass(frozen=True, slots=True)
class PostRequest(object):
    """Do a post request."""

    _requests = requests

    @safe
    def __call__(
        self,
        url: str,
        url_params: dict,
        payload: dict,
        timeout: int = 10,
    ) -> requests.Response:
        """Do post call."""
        response = self._requests.post(
            url,
            params=url_params,
            json=payload,
            timeout=timeout,
        )

        response.raise_for_status()

        return response


@final
@dataclass(frozen=True, slots=True)
class GetRequest(object):
    """Do a post request."""

    _requests = requests

    @safe
    def __call__(
        self,
        url: str,
        url_params: Optional[dict] = None,
        timeout: int = 10,
    ) -> requests.Response:
        """Do get call."""
        response = self._requests.get(
            url,
            params=url_params,
            timeout=timeout,
        )
        response.raise_for_status()

        return response


@final
@dataclass(frozen=True, slots=True)
class GetCountryCode(object):
    """Get Country code from string."""

    # dependiencies, country package
    _countries = countries

    def __call__(self, code: str) -> ResultE[str]:
        """Find country by code or name."""
        return flow(
            str(code).strip(),
            self._get,
            alt(lambda _: KeyError(  # type: ignore
                'No country found with: "{0}"'.format(code),
            )),
        )

    @safe
    def _get(self, code: str) -> str:
        return self._countries.get(code)


@final
@dataclass(frozen=True, slots=True)
class ReadLocalFile(object):
    """
    Reads local file.

    :param file_path: path to the file to read.
    :type file_path: str

    :parm mode: read mode, r = read string, rb =read bytes.
    :type mode: str

    :return: Success[bytes], Success[str], Failure[Exception]
    :rtype: bytes, str
    """

    @overload
    def __call__(
        self, file_path: str, mode: Literal['r'],
    ) -> ResultE[str]:
        """When 'r' is supplied we return 'str'."""

    @overload  # noqa: WPS440, F811
    def __call__(
        self, file_path: str, mode: Literal['rb'],
    ) -> ResultE[bytes]:
        """When 'rb' is supplied we return 'bytes' instead of a 'str'."""

    @overload  # noqa: WPS440, F811
    def __call__(self, file_path: str, mode: str) -> ResultE[Any]:
        """Any other options might return Any-thing!."""

    @safe  # noqa: WPS440, F811
    def __call__(self, file_path: str, mode: str) -> Any:
        """Open the file and return its contents."""
        with open(file_path, mode) as data_file:
            return data_file.read()


@final
@dataclass(frozen=True, slots=True)
class WriteLocalFile(object):
    """
    Writes local file.

    :param string_data: Data to write to file
    :type string_data: str
    :param file_path: writes file to this path.
    :type file_path: str

    :return: Success[bytes], Success[str], Failure[Exception]
    :rtype: bytes, str
    """

    @safe  # noqa: WPS440, F811
    def __call__(self, raw_data: str, file_path: str) -> bool:
        """Open the file and return its contents."""
        with open(file_path, 'w') as data_file:
            data_file.write(raw_data)
        return True


@final
@dataclass(frozen=True, slots=True)
class ConfigureLogging(object):
    """Configure logging."""

    _log = logging.getLogger()

    def __call__(self):
        """Set file logger and stream logger."""
        self._log.setLevel(logging.DEBUG)

        fh = logging.FileHandler('p360_contact_manager.log')
        fh.setLevel(logging.INFO)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        )
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        self._log.addHandler(fh)
        self._log.addHandler(sh)
        self._log.info('logging initialized')
