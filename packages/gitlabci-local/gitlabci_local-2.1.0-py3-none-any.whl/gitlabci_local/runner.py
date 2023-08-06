#!/usr/bin/env python3

# Standard libraries
from os import chmod, environ, stat, system
from os.path import expandvars
from pathlib import Path, PurePosixPath
from signal import getsignal, SIGINT, signal, SIGTERM
from stat import S_IRGRP, S_IROTH, S_IXGRP, S_IXOTH, S_IXUSR
from sys import stdout
from tempfile import NamedTemporaryFile
from time import sleep, time

# Modules libraries
from colored import attr, fg

# Components
from .engines.engine import Engine
from .system.platform import Platform
from .types.lists import Lists
from .types.paths import Paths
from .types.volumes import Volumes

# Constants
__MARKER_DEBUG = '__GITLAB_CI_LOCAL_DEBUG__'
__MARKER_RESULT = '__GITLAB_CI_LOCAL_RESULT__'

# Variables
__engine = None # pylint: disable=invalid-name

# Launcher
def launcher(options, jobs):

    # Variables
    jobs_status = {'jobs_count': 0, 'quiet': True, 'time_launcher': time()}
    result = None

    # Run selected jobs
    for job in jobs:

        # Filter jobs list
        if not options.pipeline and not Lists.match(options.names, job, options.no_regex):
            continue

        # Filter stages list
        if options.pipeline and options.names and not Lists.match(
                options.names, jobs[job]['stage'], options.no_regex):
            continue

        # Filter manual jobs
        job_manual = (jobs[job]['when'] == 'manual')
        if job_manual and not options.manual and not Lists.match(
                options.names, job, options.no_regex):
            continue

        # Filter disabled jobs
        if jobs[job]['options']['disabled']:
            continue

        # Raise initial result
        if result is None:
            result = True

        # Run job
        attempt = 0
        expected = result
        jobs_status['jobs_count'] += 1
        result = runner(options, jobs[job], result, jobs_status)

        # Retry job if allowed
        if expected and not result and jobs[job]['retry'] > 0:
            while not result and attempt < jobs[job]['retry']:
                attempt += 1
                result = runner(options, jobs[job], expected, jobs_status)

    # Non quiet jobs
    if not jobs_status['quiet']:

        # Pipeline jobs footer
        if jobs_status['jobs_count'] > 1:

            # Evaluate duration total time
            time_total_duration = time() - jobs_status['time_launcher']
            time_total_seconds = '%.0f second%s' % (time_total_duration % 60, 's' if
                                                    time_total_duration % 60 > 1 else '')
            time_total_minutes = ''
            if time_total_duration >= 60:
                time_total_minutes = '%.0f minute%s ' % (
                    time_total_duration / 60, 's' if time_total_duration / 60 > 1 else '')
            time_total_string = time_total_minutes + time_total_seconds

            # Final footer
            print(' %s> Pipeline: %s in %s total%s' %
                  (fg('yellow') + attr('bold'), attr('reset') + attr('bold') +
                   'Success' if result else fg('red') + attr('bold') + 'Failure',
                   time_total_string, attr('reset')))
            print(' ')
            print(' ', flush=True)

        # Simple job footer
        else:
            print(' ', flush=True)

    # Result
    return bool(result)

# Runner
def runner(options, job_data, last_result, jobs_status):

    # Globals
    global __engine # pylint: disable=global-statement,invalid-name

    # Variables
    host = False
    quiet = options.quiet
    real_paths = options.real_paths and Platform.IS_LINUX
    result = False
    time_start = time()

    # Filter when
    if last_result and job_data['when'] not in ['on_success', 'manual', 'always']:
        return last_result
    if not last_result and job_data['when'] not in ['on_failure']:
        return last_result

    # Prepare image
    image = job_data['image']

    # Prepare local runner
    if options.host or job_data['options']['host']:
        image = 'local'
        host = True

    # Prepare quiet runner
    if job_data['options']['quiet']:
        quiet = True
    elif jobs_status['quiet']:
        jobs_status['quiet'] = False

    # Prepare network
    network = 'bridge'
    if options.network:
        network = options.network

    # Prepare engine execution
    if not host:
        if __engine is None:
            __engine = Engine(options)
        engine_type = __engine.name()

    # Prepare native execution
    else:
        engine_type = 'native'

    # Header
    if not quiet:
        if jobs_status['jobs_count'] > 1:
            print(' ')
        print(' %s===[ %s%s: %s%s %s(%s, %s) %s]===%s' %
              (fg('green') + attr('bold'), fg('yellow') + attr('bold'), job_data['stage'],
               fg('yellow') + attr('bold'), job_data['name'], fg('cyan') + attr('bold'),
               image, engine_type, fg('green') + attr('bold'), attr('reset')))
        print(' ', flush=True)

    # Acquire project paths
    path_project = Paths(options.path).resolve()
    path_parent = Paths(Path(options.path).parent).resolve()

    # Acquire project targets
    if real_paths:
        target_project = path_project
        target_parent = path_parent
    else:
        target_project = Paths(Platform.BUILDS_DIR / Path(path_project).name).get()
        target_parent = Paths(Platform.BUILDS_DIR).get()

    # Prepare working directory
    if options.workdir:
        if options.workdir.startswith('.local:'):
            workdir = options.workdir[len('.local:'):]
            if host or real_paths:
                target_workdir = Paths((options.path / workdir).resolve()).get()
            else:
                target_workdir = Paths(PurePosixPath(target_project) / workdir).get()
        else:
            if host or real_paths:
                target_workdir = Paths((Path('.') / options.workdir).resolve()).get()
            else:
                target_workdir = Paths(
                    PurePosixPath(target_project) / options.workdir).get()
    elif host or real_paths:
        target_workdir = Paths(options.path).get()
    else:
        target_workdir = target_project

    # Prepare entrypoint and scripts
    entrypoint = job_data['entrypoint']
    scripts_after = []
    scripts_before = []
    scripts_commands = []
    scripts_debug = []

    # Prepare before_scripts
    if options.before:
        scripts_before += job_data['before_script']

    # Prepare scripts
    scripts_commands += job_data['script']
    if not host:
        if options.bash:
            scripts_commands = []
        if options.bash or options.debug:
            scripts_debug += ['echo "' + __MARKER_DEBUG + '"', 'tail -f /dev/null']

    # Prepare after_scripts
    if options.after:
        scripts_after += job_data['after_script']

    # Prepare temporary script
    script_file = NamedTemporaryFile(delete=False, dir=path_parent, mode='wt',
                                     newline='\n', prefix='.tmp.entrypoint.')
    target_file = Paths(Path(target_parent) / Path(script_file.name).name).get()

    # Prepare execution context
    script_file.write('#!/bin/sh')
    script_file.write('\n')
    script_file.write('result=1')
    script_file.write('\n')

    # Prepare host working directory
    if host:
        script_file.write('cd "%s"' % target_workdir)
        script_file.write('\n')

    # Prepare before_script/script context
    script_file.write('(')
    script_file.write('\n')
    if job_data['options']['silent']:
        script_file.write('set -e')
    else:
        script_file.write('set -ex')
    script_file.write('\n')

    # Prepare before_script commands
    if len(scripts_before) > 0:
        script_file.write('{')
        script_file.write('\n')
        script_file.write('\n'.join(scripts_before))
        script_file.write('\n')
        script_file.write('} && ')
        script_file.flush()

    # Prepare script commands
    if len(scripts_commands) > 0:
        script_file.write('{')
        script_file.write('\n')
        script_file.write('\n'.join(scripts_commands))
        script_file.write('\n')
        script_file.write('}')
        script_file.flush()
    else:
        script_file.write('false')
        script_file.flush()

    # Finish before_script/script context
    script_file.write('\n')
    script_file.write(') 2>&1')
    script_file.write('\n')
    script_file.write('result=${?}')
    script_file.flush()

    # Prepare debug script commands
    if len(scripts_debug) > 0:
        script_file.write('\n')
        script_file.write('(')
        script_file.write('\n')
        if not job_data['options']['silent']:
            script_file.write('set -x')
        script_file.write('\n')
        script_file.write('\n'.join(scripts_debug))
        script_file.write('\n')
        script_file.write(') 2>&1')
        script_file.flush()

    # Prepare after_script commands
    if len(scripts_after) > 0:
        script_file.write('\n')
        script_file.write('(')
        script_file.write('\n')
        if job_data['options']['silent']:
            script_file.write('set -e')
        else:
            script_file.write('set -ex')
        script_file.write('\n')
        script_file.write('{')
        script_file.write('\n')
        script_file.write('\n'.join(scripts_after))
        script_file.write('\n')
        script_file.write('}')
        script_file.write('\n')
        script_file.write(') 2>&1')
        script_file.flush()

    # Prepare container result
    if not host:
        script_file.write('\n')
        script_file.write('echo "%s:${result}"' % (__MARKER_RESULT))

    # Prepare execution result
    script_file.write('\n')
    script_file.write('exit "${result}"')
    script_file.write('\n')

    # Prepare script execution
    script_stat = stat(script_file.name)
    chmod(script_file.name, script_stat.st_mode | S_IXUSR | S_IXGRP
          | S_IRGRP | S_IROTH | S_IXOTH)
    script_file.file.close()

    # Prepare variables
    variables = dict()
    for variable in job_data['variables']:
        variables[variable] = expandvars(str(job_data['variables'][variable]))

    # Configure local variables
    variables['CI_LOCAL'] = 'true'

    # Container execution
    if not host:

        # Configure engine variables
        variables['CI_LOCAL_ENGINE_NAME'] = __engine.name()

        # Prepare volumes mounts
        volumes = Volumes()

        # Mount repository folder
        volumes.add(path_parent, target_parent, 'rw', True)

        # Extend mounts
        if options.volume:
            for volume in options.volume:
                cwd = Path('.')
                volume_local = False
                volume_nodes = volume.split(':')

                # Handle .local volumes
                if volume_nodes[0] == '.local':
                    cwd = options.path
                    volume_local = True
                    volume_nodes.pop(0)

                # Parse HOST:TARGET:MODE
                if len(volume_nodes) == 3:
                    volume_host = Paths(cwd / expandvars(volume_nodes[0])).resolve()
                    volume_target = expandvars(volume_nodes[1])
                    volume_mode = volume_nodes[2]

                # Parse HOST:TARGET
                elif len(volume_nodes) == 2:
                    volume_host = Paths(cwd / expandvars(volume_nodes[0])).resolve()
                    volume_target = expandvars(volume_nodes[1])
                    volume_mode = 'rw'

                # Parse VOLUME
                else:
                    volume_host = Paths(cwd / expandvars(volume)).resolve()
                    volume_target = Paths(cwd / expandvars(volume)).resolve()
                    volume_mode = 'rw'

                # Append volume mounts
                volumes.add(volume_host, volume_target, volume_mode, not volume_local)

        # Append sockets mounts
        if options.sockets:
            __engine.sockets(volumes)

        # Image validation
        if not image:
            raise ValueError(
                'Missing image for "%s / %s"' % (job_data['stage'], job_data['name']))
        __engine.get(image)

        # Launch container
        container = __engine.run(image, target_file, entrypoint, variables, network,
                                 volumes, target_workdir)

        # Create interruption handler
        def interrupt_handler(unused_signalnum, unused_handler):
            print(' ')
            print(' ')
            print(
                ' %s> WARNING: %sUser interruption detected, stopping the container...%s'
                % (fg('yellow') + attr('bold'), attr('reset') + attr('bold'),
                   attr('reset')))
            print(' ', flush=True)
            __engine.stop(container, 0)

        # Register interruption handler
        handler_int_original = getsignal(SIGINT)
        handler_term_original = getsignal(SIGTERM)
        signal(SIGINT, interrupt_handler)
        signal(SIGTERM, interrupt_handler)

        # Execution wrapper
        script_result = 1
        success = False

        # Show container logs
        try:
            for line in __engine.logs(container):
                if isinstance(line, bytes):
                    line_decoded = line.decode()
                    if __MARKER_DEBUG in line_decoded:
                        break
                    if __MARKER_RESULT in line_decoded:
                        script_result = int(line_decoded.split(':')[-1])
                        break
                    stdout.buffer.write(line)
                    stdout.buffer.flush()
                else:
                    if __MARKER_DEBUG in line:
                        break
                    if __MARKER_RESULT in line:
                        script_result = int(line.split(':')[-1])
                        break
                    stdout.write(line)
                    stdout.flush()
        except:
            pass

        # Runner bash or debug mode
        if options.bash or options.debug:

            # Select shell
            shell = 'sh'
            if __engine.supports(container, 'bash'):
                shell = 'bash'

            # Acquire container informations
            container_exec = __engine.help('exec')
            container_name = __engine.name(container)

            # Footer debugging informations
            print(' ')
            print(
                ' %s> INFORMATION: %sUse \'%s%s %s %s%s\' commands for debugging. Interrupt with Ctrl+C...%s'
                % (fg('yellow') + attr('bold'), attr('reset') + attr('bold'), fg('cyan'),
                   container_exec, container_name, shell, attr('reset') + attr('bold'),
                   attr('reset')))
            print(' ', flush=True)

        # Check container status
        success = __engine.wait(container, script_result)

        # Stop container
        __engine.stop(container, 0)
        sleep(0.1)

        # Remove container
        __engine.remove(container)

        # Unregister interruption handler
        signal(SIGINT, handler_int_original)
        signal(SIGTERM, handler_term_original)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

    # Native execution
    else:

        # Prepare environment
        _environ = dict(environ)
        environ.update(variables)

        # Native execution
        scripts = []
        if entrypoint:
            scripts += entrypoint
        if not scripts:
            scripts = ['sh']
        scripts += ['"%s"' % script_file.name]
        success = (system(' '.join(scripts)) == 0)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

        # Restore environment
        environ.clear()
        environ.update(_environ)

    # Close temporary script
    Path(script_file.name).unlink()

    # Initial job details
    job_details = ''
    job_details_list = []

    # Prepare when details
    if job_data['when'] not in ['on_success']:
        job_details_list += ['when: %s' % (job_data['when'])]

    # Prepare allow_failure details
    if job_data['allow_failure']:
        job_details_list += ['failure allowed']

    # Prepare job details
    if job_details_list:
        job_details = ' (' + ', '.join(job_details_list) + ')'

    # Evaluate duration time
    time_duration = time() - time_start
    time_seconds = '%.0f second%s' % (time_duration % 60,
                                      's' if time_duration % 60 > 1 else '')
    time_minutes = ''
    if time_duration >= 60:
        time_minutes = '%.0f minute%s ' % (time_duration / 60,
                                           's' if time_duration / 60 > 1 else '')
    time_string = time_minutes + time_seconds

    # Footer
    print(' ', flush=True)
    if not quiet:
        print(' %s> Result: %s in %s%s%s' %
              (fg('yellow') + attr('bold'), fg('green') + attr('bold') +
               'Success' if result else fg('red') + attr('bold') + 'Failure', time_string,
               fg('cyan') + attr('bold') + job_details, attr('reset')))
        print(' ', flush=True)

    # Allowed failure result
    if job_data['when'] not in ['on_failure', 'always'
                                ] and not result and job_data['allow_failure']:
        result = True

    # Result
    return result
