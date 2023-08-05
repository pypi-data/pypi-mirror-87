#!/usr/bin/env python3

# Libraries
import docker

# Components
from ..const import Platform

# Docker class
class Docker:

    # Members
    _client = None

    # Constructor
    def __init__(self):

        # Engine client
        self._client = docker.from_env()
        self._client.ping()

    # Exec
    def exec(self, container, command):

        # Execute command in container
        return container.exec_run(command)

    # Help
    def help(self, command):

        # Exec command
        if command is 'exec':
            return 'docker exec -it'

        # Default fallback
        return ''

    # Get
    def get(self, image):

        # Validate image exists
        try:
            self._client.images.get(image)

        # Pull missing image
        except docker.errors.ImageNotFound:
            self.pull(image)

    # Logs
    def logs(self, container):

        # Return logs stream
        return container.logs(stream=True)

    # Name
    def name(self, container):

        # Result
        return container.name

    # Pull
    def pull(self, image):

        # Pull image with logs stream
        for data in self._client.api.pull(image, stream=True, decode=True):

            # Layer progress logs
            if 'progress' in data:
                if Platform.IS_TTY_STDOUT:
                    print(
                        '\r\033[K%s: %s %s' %
                        (data['id'], data['status'], data['progress']), end='',
                        flush=True)

            # Layer event logs
            elif 'progressDetail' in data:
                if Platform.IS_TTY_STDOUT:
                    print('\r\033[K%s: %s' % (data['id'], data['status']), end='',
                          flush=True)

            # Layer completion logs
            elif 'id' in data:
                print('\r\033[K%s: %s' % (data['id'], data['status']), flush=True)

            # Image logs
            else:
                print('\r\033[K%s' % (data['status']), flush=True)

        # Footer
        print(' ', flush=True)

    # Remove
    def remove(self, container):

        # Remove container
        container.remove(force=True)

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):

        # Run container image
        return self._client.containers.run(
            image, command=command, detach=True, entrypoint=entrypoint,
            environment=variables, network_mode=network, privileged=True, remove=False,
            stdout=True, stderr=True, stream=True, volumes=volumes.get(),
            working_dir=directory)

    # Sockets
    def sockets(self, volumes):

        # Add socket volume
        if not Platform.IS_WINDOWS:
            volumes.add('/var/run/docker.sock', '/var/run/docker.sock', 'rw', True)

    # Stop
    def stop(self, container, timeout):

        # Stop container
        container.stop(timeout=timeout)

    # Supports
    def supports(self, image, container, binary):

        # Validate binary support
        exit_code, output = self.exec(container, 'whereis %s' % (binary))

        # Result
        return exit_code == 0

    # Wait
    def wait(self, container, result):

        # Wait container
        result = container.wait()

        # Result
        return result['StatusCode'] == 0
