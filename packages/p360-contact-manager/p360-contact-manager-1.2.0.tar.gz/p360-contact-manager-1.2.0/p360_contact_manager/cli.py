# -*- coding: utf-8 -*-

"""Package to get list of duplicate enterprises in ContactService API."""

import logging
import sys

from dependencies import Injector

from p360_contact_manager.api import p360
from p360_contact_manager.arguments import ArgsParser
from p360_contact_manager.common import ConfigureLogging, ReadLocalFile
from p360_contact_manager.environment_variables import (
    ParseEnvironmentVariables,
)
from p360_contact_manager.injected import injected_functions
from p360_contact_manager.settings import LoadSettings


def _get_settings() -> dict:
    # load args, envs and settings
    args = ArgsParser()(sys.argv[1:]).unwrap()
    env_vars = ParseEnvironmentVariables()().unwrap()
    settings = LoadSettings()().unwrap()

    # Update with env vars then args to overwrite
    settings.update(env_vars)
    settings.update(args)
    return settings


def main():
    """Run application."""
    ConfigureLogging()()
    log = logging.getLogger('main')

    settings = _get_settings()

    # initialize DI scope with our settings
    scope = Injector.let(**settings)

    log.info('Starting program')
    log.debug('settings: %s', scope)
    log.info('action: %s', settings.get('action'))
    action = (scope & injected_functions[settings['action']])
    if settings.get('cached'):
        log.info('Using cached data')
        action = action.let(
            get_all_enterprises=p360.GetAllCachedEnterprises,
            read=ReadLocalFile,
        )

    log.info('result: %s', action.run())


if __name__ == '__main__':
    main()  # type: ignore
