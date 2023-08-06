#!/usr/bin/env python3

# Standard libraries
from sys import version_info

# Modules libraries
from pkg_resources import require

# Components
from ..system.platform import Platform

# Version class
class Version:

    # Getter
    @staticmethod
    def get():

        # Acquire version
        name = __name__.split('.')[0]
        version = require(name)[0].version

        # Result
        return version

    # Path
    @staticmethod
    def path():

        # Acquire path
        path = __file__

        # Strip package path
        index = path.rfind(Platform.PATH_SEPARATOR)
        index = path.rfind(Platform.PATH_SEPARATOR, 0, index)
        path = path[0:index]

        # Result
        return path

    # Python
    @staticmethod
    def python():

        # Acquire Python version
        version = '%s.%s' % (version_info.major, version_info.minor)

        # Result
        return version
