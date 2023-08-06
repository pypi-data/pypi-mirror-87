#!/usr/bin/env python3

# Standard libraries
from os import sep
from pathlib import Path, PurePosixPath
from sys import platform, stdin, stdout

# Platform
class Platform:

    # Constants
    IS_LINUX = (platform in ['linux', 'linux2'])
    IS_MAC_OS = (platform in ['darwin'])
    IS_WINDOWS = (platform in ['win32', 'win64'])

    # Paths
    BUILDS_DIR = PurePosixPath('/builds')

    # Separators
    PATH_SEPARATOR = sep

    # TTYs
    IS_TTY_STDIN = stdin.isatty() and stdin.encoding != 'cp1252'
    IS_TTY_STDOUT = stdout.isatty()

    # Flush
    @staticmethod
    def flush():
        print('', flush=Platform.IS_TTY_STDOUT, end='')

    # Userspace
    @staticmethod
    def userspace(name):

        # Windows userspace
        if Platform.IS_WINDOWS:
            return Path.home() / 'AppData' / 'Local' / name

        # macOS userspace
        if Platform.IS_MAC_OS:
            return Path.home() / 'Library' / 'Preferences' / name

        # Linux userspace
        return Path.home() / '.config' / name
