#!/usr/bin/env python3

# Standard libraries
from configparser import ConfigParser

# Components
from ..system.platform import Platform

# Settings class
class Settings:

    # Constants
    SETTINGS_FILE = 'settings.ini'

    # Members
    __folder = None
    __path = None
    __settings = None

    # Constructor
    def __init__(self, name):

        # Prepare paths
        self.__folder = Platform.userspace(name)
        self.__path = self.__folder / Settings.SETTINGS_FILE

        # Parse settings
        self.__settings = ConfigParser()
        self.__settings.read(self.__path)

        # Prepare missing settings
        try:
            if self.get('package', 'name') != name:
                raise ValueError('Missing settings files')
        except:
            self.__folder.mkdir(parents=True, exist_ok=True)
            self.__reset(name)

    # Reset
    def __reset(self, name):

        # Prepare barebone settings
        self.__settings = ConfigParser()
        self.set('package', 'name', name)

    # Writer
    def __write(self):

        # Write initial settings
        with open(self.__path, 'w') as output:
            self.__settings.write(output)

    # Get
    def get(self, group, key):

        # Get settings key in group
        if group in self.__settings and key in self.__settings[group]:
            return self.__settings[group][key]

        # Default fallback
        return None

    # Set
    def set(self, group, key, value):

        # Prepare group
        if not group in self.__settings:
            self.__settings[group] = dict()

        # Set key
        self.__settings[group][key] = str(value)

        # Write updated settings
        self.__write()
