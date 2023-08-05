#!/usr/bin/env python3

# Libraries
import os
import stat
import subprocess
import tempfile
import time

# Podman class
class Podman:

    # Members
    _binary = 'podman'

    # Constructor
    def __init__(self):

        # Configure binary
        if 'PODMAN_BINARY_PATH' in os.environ:
            self._binary = os.environ['PODMAN_BINARY_PATH']

        # Check engine support
        result = self.__exec(['system', 'info'], True)
        if result.returncode != 0:
            raise NotImplementedError('Unsupported Podman engine...')

    # Internal execution
    def __exec(self, arguments, quiet=False):
        if quiet:
            return subprocess.run([self._binary] + arguments, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        else:
            return subprocess.run([self._binary] + arguments, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    # Internal watcher
    def __watch(self, arguments):
        return iter(
            subprocess.Popen([self._binary] + arguments,
                             stdout=subprocess.PIPE).stdout.readline, b'')

    # Exec
    def exec(self, container, command):

        # Adapt command
        if isinstance(command, str):
            command = [command]

        # Execute command in container
        return self.__exec(['exec', container] + command)

    # Help
    def help(self, command):

        # Exec command
        if command is 'exec':
            if 'SUDO_USER' in os.environ:
                return 'sudo podman exec -it'
            else:
                return 'podman exec -it'

        # Default fallback
        return ''

    # Get
    def get(self, image):

        # Validate image exists
        result = self.__exec(['inspect', '--type', 'image', '--format', 'exists', image],
                             True)

        # Pull missing image
        if result.returncode != 0:
            self.pull(image)

    # Logs
    def logs(self, container):

        # Return logs stream
        return self.__watch(['logs', '--follow', container])

    # Name
    def name(self, container):

        # Result
        result = self.__exec(
            ['inspect', '--type', 'container', '--format', '{{.Name}}', container])
        return result.stdout.strip().decode('utf-8') if result.returncode == 0 else ''

    # Pull
    def pull(self, image):

        # Header
        print('Pulling from %s' % (image), flush=True)

        # Pull image with logs stream
        result = self.__exec(['pull', image])

        # Layer completion logs
        if result.returncode == 0:
            result = self.__exec(
                ['inspect', '--type', 'image', '--format', '{{.Id}}', image])
            print('Digest: %s' % (result.stdout.strip().decode('utf-8')))
            print('Status: Image is up to date for %s' % (image))
        else:
            print('Status: Image not found for %s' % (image), flush=True)
            raise FileNotFoundError(result.stderr.decode('utf-8').replace('\\n', '\n'))

        # Footer
        print(' ', flush=True)

    # Remove
    def remove(self, container):

        # Remove container
        self.__exec(['rm', '--force', container])

    # Run
    def run(self, image, command, entrypoint, variables, network, volumes, directory):

        # Variables
        args_command = []
        args_entrypoint = []
        args_env = []
        args_volumes = []

        # Adapt command
        if isinstance(command, list):
            args_command = command
        elif isinstance(command, str):
            args_command = [command]

        # Adapt entrypoint
        if isinstance(entrypoint, list):
            if len(entrypoint) > 1:
                args_command = [' '.join(args_command)]
                args_command[0:0] = entrypoint[1:]
            entrypoint = entrypoint[0]
        if isinstance(entrypoint, str):
            args_entrypoint = ['--entrypoint', entrypoint]

        # Adapt mounts
        if volumes and isinstance(volumes.get(), dict):
            for volume in volumes.get().items():
                options = ''
                if volume[1]['mode'] == 'ro':
                    options += ':ro'
                elif volume[1]['mode'] == 'rw':
                    options += ':rw'
                args_volumes += [
                    '--volume',
                    '%s:%s%s' % (volume[0], volume[1]['bind'], options)
                ]

        # Adapt variables
        for variable in variables:
            args_env.extend(['--env', '%s=%s' % (variable, variables[variable])])

        # Create container image
        result = self.__exec(['create'] + args_entrypoint + args_env + ['--tty'] +
                             args_volumes + ['--privileged'] +
                             ['--security-opt', 'label=disable'] +
                             ['--workdir', directory] + [image] + args_command)
        if result.returncode == 0:
            container = result.stdout.strip().decode('utf-8')

        # Handle failures
        else:
            raise NotImplementedError(result.stderr.decode('utf-8').replace('\\n', '\n'))

        # Start container
        self.__exec(['start', container])

        # Result
        return container

    # Sockets
    def sockets(self, volumes):
        pass

    # Stop
    def stop(self, container, timeout):

        # Stop container
        self.__exec(['stop', '--time', str(timeout), container])

    # Supports
    def supports(self, image, container, binary):

        # Validate binary support
        result = self.exec(container, ['whereis', binary])

        # Result
        return result.returncode == 0

    # Wait
    def wait(self, container, result):

        # Wait container
        result = self.__exec(['wait', container])

        # Result
        return int(result.stdout.strip()) == 0 if result.returncode == 0 else False
