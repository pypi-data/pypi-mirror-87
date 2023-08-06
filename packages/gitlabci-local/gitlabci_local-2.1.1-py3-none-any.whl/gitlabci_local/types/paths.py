#!/usr/bin/env python3

# Standard libraries
from pathlib import Path, PurePosixPath

# Components
from ..system.platform import Platform

# Paths class
class Paths:

    # Members
    __path = None

    # Constructor
    def __init__(self, data):
        self.__path = data

    # Getter
    def get(self):

        # POSIX path
        path = PurePosixPath(self.__path)

        # Result
        return str(path)

    # Resolver
    def resolve(self):

        # Resolve path
        path = Path(self.__path).resolve()

        # Linux, macOS or Windows path
        if Platform.IS_LINUX or Platform.IS_MAC_OS or Platform.IS_WINDOWS:
            path = str(path)

        # Result
        return path
