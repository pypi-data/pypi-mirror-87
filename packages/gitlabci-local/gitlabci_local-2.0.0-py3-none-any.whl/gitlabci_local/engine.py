#!/usr/bin/env python3

# Libraries
from enum import Enum
import os

# Components
from .engines import docker, podman

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

    # Getter
    def get(override):

        # Default prioritized names
        defaults = [
            Names.PODMAN,
            Names.DOCKER,
        ]

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
                        names += [name for name in defaults if name.startswith(item)]
            if auto or override[-1] == ',':
                names = names + defaults
            names = list(dict.fromkeys(names))

        # Use engine defaults
        else:
            names = defaults

        # Result
        return names

# Supported engines
def supported():
    return [
        Names.AUTO,
        Names.DOCKER,
        Names.PODMAN,
    ]

# Engine class
class Engine:

    # Members
    _backend = Backend.UNKNOWN
    _engine = None
    _name = None

    # Constructor
    def __init__(self, options):

        # Acquire engine names
        names = Names.get(options.engine)

        # Iterate through names
        for name in names:

            # Podman engine detection
            if name == Names.PODMAN:
                try:
                    self._engine = podman.Podman()
                    self._backend = Backend.PODMAN
                    self._name = Names.PODMAN
                    break
                except:
                    self._engine = None

            # Docker engine detection
            elif name == Names.DOCKER:
                try:
                    self._engine = docker.Docker()
                    self._backend = Backend.DOCKER
                    self._name = Names.DOCKER
                    break
                except:
                    self._engine = None

        # Unknown engine fallback
        if not self._engine:
            raise NotImplementedError('Unknown or unsupported container engine...')

    # Exec
    def exec(self, container, command):
        return self._engine.exec(container, command)

    # Help
    def help(self, command):
        return self._engine.help(command)

    # Get
    def get(self, image):
        self._engine.get(image)

    # Logs
    def logs(self, container):
        return self._engine.logs(container)

    # Name
    def name(self, container=None):
        if container:
            return self._engine.name(container)
        else:
            return self._name

    # Pull
    def pull(self, image):
        self._engine.pull(image)

    # Remove
    def remove(self, container):
        self._engine.remove(container)

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):
        return self._engine.run(image, command, entrypoint, variables, network, volumes,
                                directory)

    # Sockets
    def sockets(self, volumes):
        self._engine.sockets(volumes)

    # Stop
    def stop(self, container, timeout):
        self._engine.stop(container, timeout)

    # Supports
    def supports(self, image, container, binary):
        return self._engine.supports(image, container, binary)

    # Wait
    def wait(self, container, result):
        return self._engine.wait(container, result)
