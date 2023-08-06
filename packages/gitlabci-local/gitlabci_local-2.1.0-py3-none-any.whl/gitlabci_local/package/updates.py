#!/usr/bin/env python3

# Standard libraries
from os import environ
from time import localtime, sleep, strftime, time
from update_checker import pretty_date, UpdateChecker

# Modules libraries
from colored import attr, fg

# Components
from .version import Version

# Updates class
class Updates:

    # Members
    __enabled = False
    __name = None
    __settings = None
    __version = None

    # Constructor
    def __init__(self, name, settings):

        # Initialize members
        self.__name = name
        self.__settings = settings
        self.__version = Version.get()

        # Acquire enabled
        enabled = self.__settings.get('updates', 'enabled')
        if not enabled:
            enabled = 1
            self.__settings.set('updates', 'enabled', enabled)

        # Check enabled
        self.__enabled = int(enabled) == 1 and 'CI_LOCAL_UPDATES_DISABLE' not in environ

    # Internal checker
    def __check(self, updates=True):

        # Check for updates
        check = UpdateChecker(bypass_cache=True).check(
            self.__name, self.__version if updates else '0.0.0')
        if check:

            # Show newer updates
            print(' ')
            print(' %sINFO: %s%s %s was released%s %s(current version is %s)%s' %
                  (fg('yellow') + attr('bold'), fg('green') + attr('bold'), self.__name,
                   check.available_version,
                   ' ' + pretty_date(check.release_date) if check.release_date else '',
                   attr('reset') + attr('bold'), self.__version, attr('reset')))
            print(' ', flush=True)
            return True

        # Failure upon check
        if not updates:

            # Show current updates
            print(' ')
            print(
                ' %sWARNING: %s%s was not found, network might be down %s(current version is %s)%s'
                % (fg('yellow') + attr('bold'), fg('red') + attr('bold'), self.__name,
                   attr('reset') + attr('bold'), self.__version, attr('reset')))
            print(' ', flush=True)
            return True

        # Result
        return False

    # Checker
    def check(self, internal=True):

        # Check for updates
        if self.__check():

            # Delay user prompt
            if internal:
                sleep(3)

        # Show current version
        elif not internal:
            self.__check(False)

    # Daily
    def daily(self):

        # Acquire updates check last timestamp
        last = self.__settings.get('updates', 'last_timestamp')

        # Handle daily checks
        current = int(time())
        if not last or strftime('%Y-%m-%d', localtime(current)) != strftime(
                '%Y-%m-%d', localtime(int(last))):
            self.__settings.set('updates', 'last_timestamp', current)
            return True

        # Default fallback
        return False

    # Enabled
    def enabled(self):
        return self.__enabled
