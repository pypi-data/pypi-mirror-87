#!/usr/bin/env python3

# Components
from .const import Platform

# Volumes class
class Volumes:

    # Members
    _volumes = None

    # Constructor
    def __init__(self):
        self._volumes = dict()

    # Add
    def add(self, source, target, mode, override):

        # Handle overrides
        if target in [self._volumes[volume]['bind'] for volume in self._volumes]:
            if not override:
                return
            else:
                duplicates = [
                    volume for volume in self._volumes
                    if self._volumes[volume]['.source'] == source
                    and self._volumes[volume]['bind'] == target
                ]
                if duplicates:
                    self._volumes.pop(duplicates[0])

        # Adapt source to allow duplicates
        while source in self._volumes:
            if Platform.IS_WINDOWS:
                source = source + Platform.PATH_SEPARATOR + '.'
            else:
                source = Platform.PATH_SEPARATOR + '.' + source

        # Add volume binding
        self._volumes[source] = { #
            'bind': target,
            'mode': mode,
            '.source': source
        }

    # Get
    def get(self):
        return self._volumes
