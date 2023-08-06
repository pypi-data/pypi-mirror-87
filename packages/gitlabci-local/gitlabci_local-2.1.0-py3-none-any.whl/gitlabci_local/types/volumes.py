#!/usr/bin/env python3

# Components
from ..system.platform import Platform

# Volumes class
class Volumes:

    # Members
    __volumes = None

    # Constructor
    def __init__(self):
        self.__volumes = dict()

    # Add
    def add(self, source, target, mode, override):

        # Handle overrides
        if target in [self.__volumes[volume]['bind'] for volume in self.__volumes]:
            if not override:
                return

            duplicates = [
                volume for volume in self.__volumes
                if self.__volumes[volume]['.source'] == source
                and self.__volumes[volume]['bind'] == target
            ]
            if duplicates:
                self.__volumes.pop(duplicates[0])

        # Adapt source to allow duplicates
        while source in self.__volumes:
            if Platform.IS_WINDOWS:
                source = source + Platform.PATH_SEPARATOR + '.'
            else:
                source = Platform.PATH_SEPARATOR + '.' + source

        # Add volume binding
        self.__volumes[source] = { #
            'bind': target,
            'mode': mode,
            '.source': source
        }

    # Get
    def get(self):
        return self.__volumes
