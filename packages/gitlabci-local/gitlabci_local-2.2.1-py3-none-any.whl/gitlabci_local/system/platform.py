#!/usr/bin/env python3

# Standard libraries
from os import environ, sep
from os.path import expanduser
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

    # Users
    IS_USER_SUDO = 'SUDO_USER' in environ
    USER_SUDO = environ['SUDO_USER'] if IS_USER_SUDO else ''

    # Flush
    @staticmethod
    def flush():
        print('', flush=Platform.IS_TTY_STDOUT, end='')

    # Userspace
    @staticmethod
    def userspace(name):

        # Variables
        home = None

        # Elevated home
        if Platform.IS_USER_SUDO:
            home = Path(expanduser('~%s' % (Platform.USER_SUDO)))

        # Default home
        if not home or not home.is_dir():
            home = Path.home()

        # Windows userspace
        if Platform.IS_WINDOWS:
            return home / 'AppData' / 'Local' / name

        # macOS userspace
        if Platform.IS_MAC_OS:
            return home / 'Library' / 'Preferences' / name

        # Linux userspace
        return home / '.config' / name
