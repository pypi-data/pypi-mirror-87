#!/usr/bin/env python3

# Standard libraries
from enum import Enum

# Components
from . import docker, podman

# Backend enumeration
class Backend(Enum):
    DOCKER = 1
    PODMAN = 2
    UNKNOWN = 3

# Names enumeration
class Names:

    # Constants
    AUTO = 'auto'
    DOCKER = 'docker'
    PODMAN = 'podman'

    # Defaults
    DEFAULTS = [
        PODMAN,
        DOCKER,
    ]

    # Getter
    @staticmethod
    def get(override):

        # Adapt override
        override = override.lower() if override else None

        # Handle engine overrides
        if override:
            auto = False
            names = []
            overrides = override.split(',')
            for item in overrides:
                if item:
                    if Names.AUTO.startswith(item):
                        auto = True
                    else:
                        names += [
                            name for name in Names.DEFAULTS if name.startswith(item)
                        ]
            if auto or override[-1] == ',':
                names = names + Names.DEFAULTS
            names = list(dict.fromkeys(names))

        # Use engine defaults
        else:
            names = Names.DEFAULTS

        # Result
        return names

# Supported engines
def supported():
    return [Names.AUTO] + Names.DEFAULTS

# Engine class
class Engine:

    # Members
    __backend = Backend.UNKNOWN
    __engine = None
    __name = None

    # Constructor
    def __init__(self, options):

        # Acquire engine names
        names = Names.get(options.engine)

        # Iterate through names
        for name in names:

            # Podman engine detection
            if name == Names.PODMAN:
                try:
                    self.__engine = podman.Podman()
                    self.__backend = Backend.PODMAN
                    self.__name = Names.PODMAN
                    break
                except:
                    self.__engine = None

            # Docker engine detection
            elif name == Names.DOCKER:
                try:
                    self.__engine = docker.Docker()
                    self.__backend = Backend.DOCKER
                    self.__name = Names.DOCKER
                    break
                except:
                    self.__engine = None

        # Unknown engine fallback
        if not self.__engine:
            raise NotImplementedError('Unknown or unsupported container engine...')

    # Exec
    def exec(self, container, command):
        return self.__engine.exec(container, command)

    # Help
    def help(self, command):
        return self.__engine.help(command)

    # Get
    def get(self, image):
        self.__engine.get(image)

    # Logs
    def logs(self, container):
        return self.__engine.logs(container)

    # Name
    def name(self, container=None):

        # Container name
        if container:
            return self.__engine.name(container)

        # Engine name
        return self.__name

    # Pull
    def pull(self, image):
        self.__engine.pull(image)

    # Remove
    def remove(self, container):
        self.__engine.remove(container)

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):
        return self.__engine.run(image, command, entrypoint, variables, network, volumes,
                                 directory)

    # Sockets
    def sockets(self, volumes):
        self.__engine.sockets(volumes)

    # Stop
    def stop(self, container, timeout):
        self.__engine.stop(container, timeout)

    # Supports
    def supports(self, container, binary):
        return self.__engine.supports(container, binary)

    # Wait
    def wait(self, container, result):
        return self.__engine.wait(container, result)
