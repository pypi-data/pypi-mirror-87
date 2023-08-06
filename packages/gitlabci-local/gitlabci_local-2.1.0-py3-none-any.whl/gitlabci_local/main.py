#!/usr/bin/env python3

# Standard libraries
from argparse import ArgumentParser, RawTextHelpFormatter, SUPPRESS
from os import environ
from pathlib import Path
from subprocess import check_output, DEVNULL, Popen
from sys import argv, exit

# Modules libraries
from colored import attr, fg

# Components
from .dumper import dumper
from .menu import selector
from .engines.engine import supported as engine_supported
from .package.names import ALIAS, CONFIGURATION, NAME
from .package.settings import Settings
from .package.updates import Updates
from .package.version import Version
from .parser import reader
from .puller import puller
from .runner import launcher
from .system.platform import Platform

# Main
def main():

    # Variables
    hint = ''
    interactive = Platform.IS_TTY_STDIN and Platform.IS_TTY_STDOUT
    result = False

    # Arguments creation
    parser = ArgumentParser(
        prog=NAME, description='%s: Launch %s jobs locally (aliases: %s)' %
        (NAME, CONFIGURATION, ALIAS), add_help=False,
        formatter_class=RawTextHelpFormatter)

    # Arguments default definitions
    tags_default = ['deploy', 'local', 'publish']

    # Arguments enumerations definitions
    networks_enum = ['bridge', 'host', 'none']

    # Arguments internal definitions
    parser.add_argument('-h', '--help', dest='help', action='store_true',
                        help='Show this help message')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='Show the current version')
    parser.add_argument('--update-check', dest='update_check', action='store_true',
                        help='Check for newer package updates')

    # Arguments optional definitions
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help='Hide jobs execution context')
    parser.add_argument(
        '-c', dest='configuration', default=CONFIGURATION,
        help='Path to the %s configuration file or folder' % CONFIGURATION)
    parser.add_argument('-B', '--no-before', dest='before', action='store_false',
                        help='Disable before_script executions')
    parser.add_argument('-A', '--no-after', dest='after', action='store_false',
                        help='Disable after_script executions')
    parser.add_argument('-m', '--manual', dest='manual', action='store_true',
                        help='Allow manual jobs to be used')
    parser.add_argument(
        '-n', dest='network',
        help='Configure the network mode used\nChoices: %s. Default: %s' %
        (', '.join(networks_enum), networks_enum[0]))
    parser.add_argument('-p', '--pipeline', dest='pipeline', action='store_true',
                        help='Automatically run pipeline stages rather than jobs')
    parser.add_argument('-e', dest='env', action='append',
                        help='Define VARIABLE=value, pass VARIABLE or ENV file')
    parser.add_argument(
        '-E', dest='engine',
        help='Force a specific engine (or define CI_LOCAL_ENGINE)\nDefault list: %s' %
        (','.join(engine_supported())))
    parser.add_argument('-H', '--host', dest='host', action='store_true',
                        help='Run all jobs on the host rather than containers')
    parser.add_argument('-R', '--no-regex', dest='no_regex', action='store_true',
                        help='Disable regex search of names')
    parser.add_argument(
        '-t', dest='tags', help='Handle listed tags as manual jobs\nDefault list: %s' %
        (','.join(tags_default)))
    parser.add_argument('--tags-default', dest='tags_default', action='store_true',
                        help=SUPPRESS)
    parser.add_argument('-r', '--real-paths', dest='real_paths', action='store_true',
                        help='Mount real folder paths in the container (Linux only)')
    parser.add_argument('-S', '--sockets', dest='sockets', action='store_true',
                        help='Mount engine sockets for nested containers')
    parser.add_argument('-v', dest='volume', action='append',
                        help='Mount VOLUME or HOST:TARGET in containers')
    parser.add_argument('-w', dest='workdir',
                        help='Override the container\'s working path')
    parser.add_argument('--all', dest='all', action='store_true',
                        help='Enable all jobs by default in selections')
    parser.add_argument('--defaults', dest='defaults', action='store_true',
                        help='Use default variables for .local:configurations')

    # Arguments debugging definitions
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--bash', dest='bash', action='store_true',
                       help='Prepare runners for manual bash purposes')
    group.add_argument('--debug', dest='debug', action='store_true',
                       help='Keep runners active for debugging purposes')

    # Arguments internal definitions
    parser.add_argument('--image', dest='image', help=SUPPRESS)

    # Arguments exclusive definitions
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--dump', dest='dump', action='store_true',
                       help='Dump parsed %s configuration' % CONFIGURATION)
    group.add_argument('-s', '--select', dest='select', action='store_true',
                       help='Force jobs selection from enumerated names')
    group.add_argument('-l', '--list', dest='list', action='store_true',
                       help='Select one job to run (implies --manual)')
    group.add_argument('--pull', dest='pull', action='store_true',
                       help='Pull container images from all jobs')

    # Arguments positional definitions
    parser.add_argument(
        'names', nargs='*', help=
        'Names of specific jobs (or stages with --pipeline)\nRegex names is supported unless --no-regex is used'
    )

    # Arguments parser
    options = parser.parse_args()

    # Help informations
    if options.help:
        print(' ')
        parser.print_help()
        print(' ', flush=True)
        exit(0)

    # Instantiate settings
    settings = Settings(NAME)

    # Instantiate updates
    updates = Updates(NAME, settings)

    # Version informations
    if options.version:
        print(
            '%s %s from %s (python %s)' %
            (NAME, Version.get(), Version.path(), Version.python()), flush=True)
        exit(0)

    # Check for current updates
    if options.update_check:
        updates.check(False)
        exit(0)

    # Check for daily updates
    if updates.enabled() and updates.daily():
        updates.check(True)

    # Prepare configuration
    if Path(options.configuration).is_dir():
        options.configuration = Path(options.configuration) / CONFIGURATION

    # Prepare engine
    if not options.engine and 'CI_LOCAL_ENGINE' in environ:
        options.engine = environ['CI_LOCAL_ENGINE']
    elif options.engine:
        environ['CI_LOCAL_ENGINE'] = options.engine

    # Prepare paths
    options.configuration = Path(options.configuration).resolve()
    options.path = options.configuration.parent

    # Prepare tags
    if options.tags:
        options.tags = options.tags.split(',')
    else:
        options.tags = tags_default
        options.tags_default = True

    # Read configuration
    jobs = reader(options)
    if not jobs:
        exit(1)

    # Header
    print(' ', flush=True)

    # Dump configuration
    if options.dump:
        result = dumper(options, jobs)

    # Pull jobs images
    elif options.pull:
        result = puller(options, jobs)

    # Select job
    elif options.list and interactive:
        options.manual = True
        result = selector(options, jobs)

    # Select jobs
    elif options.select and interactive:
        result = selector(options, jobs)

    # Launch pipeline
    elif options.pipeline:
        result = launcher(options, jobs)

    # Launch jobs
    elif options.names:
        result = launcher(options, jobs)

    # Select jobs
    elif interactive:
        result = selector(options, jobs)

    # Launch all jobs
    elif options.all:
        options.pipeline = True
        result = launcher(options, jobs)

    # Unsupported case
    else:

        # Windows WinPTY compatibility
        if Platform.IS_WINDOWS and not 'CI_LOCAL_WINPTY' in environ:
            hint = ' (on Windows, winpty is required)'
            try:
                winpty = check_output(['where', 'winpty.exe'], stderr=DEVNULL).strip()
            except:
                pass
            else:
                _environ = dict(environ)
                _environ['CI_LOCAL_WINPTY'] = 'true'
                process = Popen([winpty] + argv, env=_environ)
                process.wait()
                exit(process.returncode)

        # Unsupported interactive terminal
        print(' %s%s: %sERROR: %sUnsupported non-interactive context%s...%s' %
              (fg('green') + attr('bold'), NAME, fg('red') + attr('bold'),
               attr('reset') + attr('bold'), hint, attr('reset')))
        print(' ', flush=True)

    # Result
    if result:
        exit(0)
    else:
        exit(1)

# Entrypoint
if __name__ == '__main__':
    main()
