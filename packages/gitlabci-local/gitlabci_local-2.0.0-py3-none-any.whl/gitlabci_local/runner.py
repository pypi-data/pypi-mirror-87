#!/usr/bin/env python3

# Libraries
import colored
import datetime
import os
from pathlib import Path, PurePosixPath
import signal
import stat
import sys
import tempfile
import time

# Components
from .const import Platform
from .engine import Engine
from .main import NAME
from .types import Volumes
from .utils import getPath, nameCheck, resolvePath

# Constants
marker_debug = '__GITLAB_CI_LOCAL_DEBUG__'
marker_result = '__GITLAB_CI_LOCAL_RESULT__'

# Variables
engine = None

# Launcher
def launcher(options, jobs):

    # Variables
    jobs_status = {'jobs_count': 0, 'quiet': True, 'time_launcher': time.time()}
    result = None

    # Run selected jobs
    for job in jobs:

        # Filter jobs list
        if not options.pipeline and not nameCheck(job, options.names, options.no_regex):
            continue

        # Filter stages list
        if options.pipeline and options.names and not nameCheck(
                jobs[job]['stage'], options.names, options.no_regex):
            continue

        # Filter manual jobs
        job_manual = (jobs[job]['when'] == 'manual')
        if job_manual and not options.manual and not nameCheck(job, options.names,
                                                               options.no_regex):
            continue

        # Filter disabled jobs
        if jobs[job]['options']['disabled']:
            continue

        # Raise initial result
        if result == None:
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
            time_total_duration = time.time() - jobs_status['time_launcher']
            time_total_seconds = '%.0f second%s' % (time_total_duration % 60, 's' if
                                                    time_total_duration % 60 > 1 else '')
            time_total_minutes = ''
            if time_total_duration >= 60:
                time_total_minutes = '%.0f minute%s ' % (
                    time_total_duration / 60, 's' if time_total_duration / 60 > 1 else '')
            time_total_string = time_total_minutes + time_total_seconds

            # Final footer
            print(' %s> Pipeline: %s in %s total%s' %
                  (colored.fg('yellow') + colored.attr('bold'), colored.attr('reset') +
                   colored.attr('bold') + 'Success' if result else colored.fg('red') +
                   colored.attr('bold') + 'Failure', time_total_string,
                   colored.attr('reset')))
            print(' ')
            print(' ', flush=True)

        # Simple job footer
        else:
            print(' ', flush=True)

    # Result
    return True if result else False

# Runner
def runner(options, job_data, last_result, jobs_status):

    # Globals
    global engine

    # Variables
    host = False
    quiet = options.quiet
    real_paths = options.real_paths and Platform.IS_LINUX
    result = False
    time_start = time.time()
    volumes = Volumes()

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
        if engine is None:
            engine = Engine(options)
        engine_type = engine.name()

    # Prepare native execution
    else:
        engine_type = 'native'

    # Header
    if not quiet:
        if jobs_status['jobs_count'] > 1:
            print(' ')
        print(' %s===[ %s%s: %s%s %s(%s, %s) %s]===%s' %
              (colored.fg('green') + colored.attr('bold'),
               colored.fg('yellow') + colored.attr('bold'), job_data['stage'],
               colored.fg('yellow') + colored.attr('bold'), job_data['name'],
               colored.fg('cyan') + colored.attr('bold'), image, engine_type,
               colored.fg('green') + colored.attr('bold'), colored.attr('reset')))
        print(' ', flush=True)

    # Acquire project paths
    pathProject = resolvePath(options.path)
    pathParent = resolvePath(Path(options.path).parent)

    # Acquire project targets
    if real_paths:
        pathTargetProject = pathProject
        pathTargetParent = pathParent
    else:
        pathTargetProject = getPath(Platform.BUILDS_DIR / Path(pathProject).name)
        pathTargetParent = getPath(Platform.BUILDS_DIR)

    # Prepare working directory
    if options.workdir:
        if options.workdir.startswith('.local:'):
            workdir = options.workdir[len('.local:'):]
            if host or real_paths:
                pathWorkDir = getPath((options.path / workdir).resolve())
            else:
                pathWorkDir = getPath(PurePosixPath(pathTargetProject) / workdir)
        else:
            if host or real_paths:
                pathWorkDir = getPath((Path('.') / options.workdir).resolve())
            else:
                pathWorkDir = getPath(PurePosixPath(pathTargetProject) / options.workdir)
    elif real_paths:
        pathWorkDir = getPath(options.path)
    else:
        pathWorkDir = pathTargetProject

    # Prepare entrypoint and scripts
    entrypoint = job_data['entrypoint']
    scriptsAfter = []
    scriptsBefore = []
    scriptsCommands = []
    scriptsDebug = []

    # Prepare before_scripts
    if options.before:
        scriptsBefore += job_data['before_script']

    # Prepare scripts
    scriptsCommands += job_data['script']
    if not host:
        if options.bash:
            scriptsCommands = []
        if options.bash or options.debug:
            scriptsDebug += ['echo "' + marker_debug + '"', 'tail -f /dev/null']

    # Prepare after_scripts
    if options.after:
        scriptsAfter += job_data['after_script']

    # Prepare temporary script
    scriptFile = tempfile.NamedTemporaryFile(delete=False, dir=pathParent, mode='wt',
                                             newline='\n', prefix='.tmp.entrypoint.')
    scriptTargetPath = getPath(Path(pathTargetParent) / Path(scriptFile.name).name)

    # Prepare execution context
    scriptFile.write('#!/bin/sh')
    scriptFile.write('\n')
    scriptFile.write('result=1')
    scriptFile.write('\n')

    # Prepare host working directory
    if host:
        scriptFile.write('cd "%s"' % pathWorkDir)
        scriptFile.write('\n')

    # Prepare before_script/script context
    scriptFile.write('(')
    scriptFile.write('\n')
    if job_data['options']['silent']:
        scriptFile.write('set -e')
    else:
        scriptFile.write('set -ex')
    scriptFile.write('\n')

    # Prepare before_script commands
    if len(scriptsBefore) > 0:
        scriptFile.write('{')
        scriptFile.write('\n')
        scriptFile.write('\n'.join(scriptsBefore))
        scriptFile.write('\n')
        scriptFile.write('} && ')
        scriptFile.flush()

    # Prepare script commands
    if len(scriptsCommands) > 0:
        scriptFile.write('{')
        scriptFile.write('\n')
        scriptFile.write('\n'.join(scriptsCommands))
        scriptFile.write('\n')
        scriptFile.write('}')
        scriptFile.flush()
    else:
        scriptFile.write('false')
        scriptFile.flush()

    # Finish before_script/script context
    scriptFile.write('\n')
    scriptFile.write(') 2>&1')
    scriptFile.write('\n')
    scriptFile.write('result=${?}')
    scriptFile.flush()

    # Prepare debug script commands
    if len(scriptsDebug) > 0:
        scriptFile.write('\n')
        scriptFile.write('(')
        scriptFile.write('\n')
        if not job_data['options']['silent']:
            scriptFile.write('set -x')
        scriptFile.write('\n')
        scriptFile.write('\n'.join(scriptsDebug))
        scriptFile.write('\n')
        scriptFile.write(') 2>&1')
        scriptFile.flush()

    # Prepare after_script commands
    if len(scriptsAfter) > 0:
        scriptFile.write('\n')
        scriptFile.write('(')
        scriptFile.write('\n')
        if job_data['options']['silent']:
            scriptFile.write('set -e')
        else:
            scriptFile.write('set -ex')
        scriptFile.write('\n')
        scriptFile.write('{')
        scriptFile.write('\n')
        scriptFile.write('\n'.join(scriptsAfter))
        scriptFile.write('\n')
        scriptFile.write('}')
        scriptFile.write('\n')
        scriptFile.write(') 2>&1')
        scriptFile.flush()

    # Prepare container result
    if not host:
        scriptFile.write('\n')
        scriptFile.write('echo "%s:${result}"' % (marker_result))

    # Prepare execution result
    scriptFile.write('\n')
    scriptFile.write('exit "${result}"')
    scriptFile.write('\n')

    # Prepare script execution
    script_stat = os.stat(scriptFile.name)
    os.chmod(
        scriptFile.name, script_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP
        | stat.S_IRGRP | stat.S_IROTH | stat.S_IXOTH)
    scriptFile.file.close()

    # Mount repository folder
    volumes.add(pathParent, pathTargetParent, 'rw', True)

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
                volume_host = resolvePath(cwd / os.path.expandvars(volume_nodes[0]))
                volume_target = os.path.expandvars(volume_nodes[1])
                volume_mode = volume_nodes[2]

            # Parse HOST:TARGET
            elif len(volume_nodes) == 2:
                volume_host = resolvePath(cwd / os.path.expandvars(volume_nodes[0]))
                volume_target = os.path.expandvars(volume_nodes[1])
                volume_mode = 'rw'

            # Parse VOLUME
            else:
                volume_host = resolvePath(cwd / os.path.expandvars(volume))
                volume_target = resolvePath(cwd / os.path.expandvars(volume))
                volume_mode = 'rw'

            # Append volume mounts
            volumes.add(volume_host, volume_target, volume_mode, not volume_local)

    # Prepare variables
    variables = dict()
    for variable in job_data['variables']:
        variables[variable] = os.path.expandvars(str(job_data['variables'][variable]))

    # Configure local variables
    variables['CI_LOCAL'] = 'true'

    # Container execution
    if not host:

        # Configure engine variables
        variables['CI_LOCAL_ENGINE_NAME'] = engine.name()

        # Append sockets mounts
        if options.sockets:
            engine.sockets(volumes)

        # Image validation
        if not image:
            raise ValueError(
                'Missing image for "%s / %s"' % (job_data['stage'], job_data['name']))
        engine.get(image)

        # Launch container
        container = engine.run(image, scriptTargetPath, entrypoint, variables, network,
                               volumes, pathWorkDir)

        # Create interruption handler
        def interruptHandler(signal, frame):
            print(' ')
            print(' ')
            print(
                ' %s> WARNING: %sUser interruption detected, stopping the container...%s'
                % (colored.fg('yellow') + colored.attr('bold'),
                   colored.attr('reset') + colored.attr('bold'), colored.attr('reset')))
            print(' ', flush=True)
            engine.stop(container, 0)

        # Register interruption handler
        originalINTHandler = signal.getsignal(signal.SIGINT)
        originalTERMHandler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGINT, interruptHandler)
        signal.signal(signal.SIGTERM, interruptHandler)

        # Execution wrapper
        scriptResult = 1
        success = False

        # Show container logs
        try:
            for line in engine.logs(container):
                if isinstance(line, bytes):
                    line_decoded = line.decode()
                    if marker_debug in line_decoded:
                        break
                    elif marker_result in line_decoded:
                        scriptResult = int(line_decoded.split(':')[-1])
                        break
                    sys.stdout.buffer.write(line)
                    sys.stdout.buffer.flush()
                else:
                    if marker_debug in line:
                        break
                    elif marker_result in line:
                        scriptResult = int(line.split(':')[-1])
                        break
                    sys.stdout.write(line)
                    sys.stdout.flush()
        except:
            pass

        # Runner bash or debug mode
        if options.bash or options.debug:

            # Select shell
            shell = 'sh'
            if engine.supports(image, container, 'bash'):
                shell = 'bash'

            # Acquire container informations
            container_exec = engine.help('exec')
            container_name = engine.name(container)

            # Footer debugging informations
            print(' ')
            print(
                ' %s> INFORMATION: %sUse \'%s%s %s %s%s\' commands for debugging. Interrupt with Ctrl+C...%s'
                % (colored.fg('yellow') + colored.attr('bold'),
                   colored.attr('reset') + colored.attr('bold'),
                   colored.fg('cyan'), container_exec, container_name, shell,
                   colored.attr('reset') + colored.attr('bold'), colored.attr('reset')))
            print(' ', flush=True)

        # Check container status
        success = engine.wait(container, scriptResult)

        # Stop container
        engine.stop(container, 0)
        time.sleep(0.1)

        # Remove container
        engine.remove(container)

        # Unregister interruption handler
        signal.signal(signal.SIGINT, originalINTHandler)
        signal.signal(signal.SIGTERM, originalTERMHandler)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

    # Native execution
    else:

        # Prepare environment
        _environ = dict(os.environ) # or os.environ.copy()
        os.environ.update(variables)

        # Native execution
        scripts = []
        if entrypoint:
            scripts += entrypoint
        if not scripts:
            scripts = ['sh']
        scripts += ['"%s"' % scriptFile.name]
        success = (os.system(' '.join(scripts)) == 0)

        # Result evaluation
        if job_data['when'] in ['on_failure', 'always']:
            result = last_result
        elif success:
            result = True

        # Restore environment
        os.environ.clear()
        os.environ.update(_environ)

    # Close temporary script
    Path(scriptFile.name).unlink()

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
    time_duration = time.time() - time_start
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
              (colored.fg('yellow') + colored.attr('bold'), colored.fg('green') +
               colored.attr('bold') + 'Success' if result else colored.fg('red') +
               colored.attr('bold') + 'Failure', time_string, colored.fg('cyan') +
               colored.attr('bold') + job_details, colored.attr('reset')))
        print(' ', flush=True)

    # Allowed failure result
    if job_data['when'] not in ['on_failure', 'always'
                                ] and not result and job_data['allow_failure']:
        result = True

    # Result
    return result
