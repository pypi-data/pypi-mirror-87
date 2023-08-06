#!/usr/bin/env python3

# Standard libraries
from pathlib import Path, PurePosixPath

# Components
from ..system.platform import Platform

# Paths class
class Paths:

    # Getter
    @staticmethod
    def get(data):

        # POSIX path
        path = PurePosixPath(data)

        # Result
        return str(path)

    # Resolver
    @staticmethod
    def resolve(data):

        # Resolve path
        path = Path(data).resolve()

        # Linux, macOS or Windows path
        if Platform.IS_LINUX or Platform.IS_MAC_OS or Platform.IS_WINDOWS:
            path = str(path)

        # Result
        return path
