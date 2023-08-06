#!/usr/bin/env python3

# Standard libraries
from json import load as json_load
from os import environ
from pathlib import Path
from PyInquirer import prompt as PyInquirer_prompt
from PyInquirer import Separator as PyInquirer_Separator
from PyInquirer import style_from_dict as PyInquirer_style_from_dict
from PyInquirer import Token as PyInquirer_Token

# Modules libraries
from colored import attr, fg
from oyaml import safe_load as yaml_safe_load

# Components
from .package.names import NAME
from .package.patcher import Patcher
from .runner import launcher
from .system.platform import Platform
from .types.dicts import Dicts
from .types.lists import Lists

# Patch theme
Patcher()

# Selector theme
__SelectorTheme = PyInquirer_style_from_dict({
    PyInquirer_Token.Separator: '#FFFF00 bold',
    PyInquirer_Token.QuestionMark: '#FFFF00 bold',
    PyInquirer_Token.Selected: '#00FF00 bold',
    PyInquirer_Token.Instruction: '#00FFFF bold',
    PyInquirer_Token.Pointer: '#FFFF00 bold',
    PyInquirer_Token.Answer: '#00FFFF bold',
    PyInquirer_Token.Question: '#00FF00 bold',
})

# Configurations theme
__ConfigurationsTheme = PyInquirer_style_from_dict({
    PyInquirer_Token.Selected: '#00FF00 bold',
    PyInquirer_Token.Instruction: '#00FFFF bold',
    PyInquirer_Token.Pointer: '#FFFF00 bold',
    PyInquirer_Token.Answer: '#00FFFF bold',
    PyInquirer_Token.Question: '#FFFF00 bold',
})

# Selector
def selector(options, jobs):

    # Variables
    default_check = options.all
    jobs_available = False
    jobs_choices = []
    jobs_index = 0
    result = True
    stage = ''

    # Stages groups
    for job in jobs:

        # Filter names
        if options.names:

            # Filter jobs list
            if not options.pipeline and not Lists.match(options.names, job,
                                                        options.no_regex):
                continue

            # Filter stages list
            if options.pipeline and not Lists.match(options.names, jobs[job]['stage'],
                                                    options.no_regex):
                continue

        # Stages separator
        if stage != jobs[job]['stage']:
            stage = jobs[job]['stage']
            jobs_choices += [PyInquirer_Separator('\n Stage %s:' % (stage))]

        # Initial job details
        job_details = ''
        job_details_list = []

        # Disabled jobs
        disabled = False
        if jobs[job]['when'] in ['manual'] and not options.manual:
            disabled = 'Manual'
        else:
            if jobs[job]['when'] == 'manual':
                job_details_list += ['Manual']
            elif jobs[job]['when'] == 'on_failure':
                job_details_list += ['On failure']
            jobs_available = True

        # Parser disabled jobs
        if jobs[job]['options']['disabled']:
            disabled = jobs[job]['options']['disabled']

        # Failure allowed jobs
        if jobs[job]['allow_failure']:
            job_details_list += ['Failure allowed']

        # Register job tags
        tags = ''
        if jobs[job]['tags']:
            tags = ' [%s]' % (','.join(jobs[job]['tags']))

        # Prepare job details
        if job_details_list:
            job_details = ' (' + ', '.join(job_details_list) + ')'

        # Job choices
        jobs_index += 1
        jobs_choices += [{
            # 'key': str(jobs_index),
            'name': '%s%s%s' % (jobs[job]['name'], tags, job_details),
            'value': job,
            'checked': default_check,
            'disabled': disabled
        }]

    # Prepare jobs selection
    selection_type = 'list' if options.list else 'checkbox'
    selection_prompt = [{
        'type': selection_type,
        'qmark': '',
        'message': '===[ Jobs selector ]===',
        'name': 'jobs',
        'choices': jobs_choices
    }]

    # Request jobs selection
    if jobs_choices and jobs_available:
        answers = PyInquirer_prompt(selection_prompt, style=__SelectorTheme)
    else:
        print(
            ' %s%s: %sERROR: %sNo jobs found for selection%s' %
            (fg('green') + attr('bold'), NAME, fg('red') + attr('bold'),
             attr('reset') + attr('bold'), attr('reset')), flush=True)
        answers = None

    # Parse jobs selection
    if answers and 'jobs' in answers:
        options.names = answers['jobs']
    else:
        options.names = []

    # Drop pipeline mode for jobs
    options.pipeline = False

    # Footer
    print(' ')
    print(' ', flush=True)

    # Launch jobs
    if options.names:
        result = launcher(options, jobs)

    # Result
    return result

# Configurator
def configurator(options, configurations):

    # Variables
    result = dict()

    # Header
    print(' ')
    print(' %s===[ %sConfigurations menu %s]===%s' %
          (fg('green') + attr('bold'), fg('yellow') + attr('bold'),
           fg('green') + attr('bold'), attr('reset')))
    print(' ', flush=True)

    # Walk through configurations
    for variable in configurations:

        # Variables
        variable_choices = []
        variable_default = ''
        variable_index = 0
        variable_set = False
        variable_values = []

        # Extract configuration fields
        variable_node = configurations[variable]
        variable_help = variable_node['help']
        variable_type = variable_node['type']

        # Prepare configuration selection
        configuration_prompt = [{
            'name': variable,
            'qmark': '',
            'message': 'Variable %s: %s:' % (variable, variable_help),
        }]

        # Extract environment variable
        if variable in environ:
            variable_default = environ[variable]
            variable_set = True

        # Parse configuration types: boolean
        if variable_type == 'boolean':
            if 'default' in variable_node and variable_node['default'] in [
                    False, 'false'
            ]:
                variable_values = ['false', 'true']
            else:
                variable_values = ['true', 'false']
            if not variable_set:
                variable_default = variable_values[0]
            for choice in variable_values:
                variable_index += 1
                variable_choices += [{
                    # 'key': str(variable_index),
                    'name': '%s' % (choice),
                    'value': choice
                }]
            configuration_prompt[0]['type'] = 'list'
            configuration_prompt[0]['choices'] = variable_choices

        # Parse configuration types: choice
        elif variable_type == 'choice':
            variable_values = variable_node['values']
            if not variable_set:
                variable_default = variable_values[0]
            for choice in variable_values:
                variable_index += 1
                variable_choices += [{
                    'key': str(variable_index),
                    'name': '%s' % (choice),
                    'value': choice
                }]
            configuration_prompt[0]['type'] = 'list'
            configuration_prompt[0]['choices'] = variable_choices

        # Parse configuration types: input
        elif variable_type == 'input':
            configuration_prompt[0]['type'] = 'input'
            if 'default' in variable_node and variable_node[
                    'default'] and not variable_set:
                variable_default = variable_node['default']
                configuration_prompt[0]['default'] = variable_default

        # Parse configuration types: json
        elif variable_type == 'json':
            if not variable_set:
                configuration_path = Path(options.path) / variable_node['path']
                configuration_key = variable_node['key']
                with open(configuration_path, 'r') as configuration_data:
                    configuration_dict = json_load(configuration_data)
                    variable_values = Dicts.find(configuration_dict, configuration_key)
                    if not variable_values:
                        raise ValueError(
                            'Unknown "%s" key in %s for "%s"' %
                            (configuration_key, configuration_path, variable))
                    for choice in variable_values:
                        variable_index += 1
                        variable_choices += [{
                            'key': str(variable_index),
                            'name': '%s' % (choice),
                            'value': choice
                        }]
                    configuration_prompt[0]['type'] = 'list'
                    configuration_prompt[0]['choices'] = variable_values

        # Parse configuration types: yaml
        elif variable_type == 'yaml':
            if not variable_set:
                configuration_path = Path(options.path) / variable_node['path']
                configuration_key = variable_node['key']
                with open(configuration_path, 'r') as configuration_data:
                    configuration_dict = yaml_safe_load(configuration_data)
                    variable_values = Dicts.find(configuration_dict, configuration_key)
                    if not variable_values:
                        raise ValueError(
                            'Unknown "%s" key in %s for "%s"' %
                            (configuration_key, configuration_path, variable))
                    for choice in variable_values:
                        variable_index += 1
                        variable_choices += [{
                            'key': str(variable_index),
                            'name': '%s' % (choice),
                            'value': choice
                        }]
                    configuration_prompt[0]['type'] = 'list'
                    configuration_prompt[0]['choices'] = variable_values

        # Parse configuration types: unknown
        else:
            print(' ')
            print(' %s%s: %sERROR: %sUnsupported configuration type "%s"...%s' %
                  (fg('green') + attr('bold'), NAME, fg('red') + attr('bold'),
                   attr('reset') + attr('bold'), variable_type, attr('reset')))
            print(' ', flush=True)

        # Extract environment variable
        if variable in environ:
            variable_default = environ[variable]
            variable_set = True

        # Request configuration selection
        if not Platform.IS_TTY_STDIN or variable_set or options.defaults:
            result[variable] = str(variable_default)
            print(' %s%s  %s%s%s' %
                  (fg('yellow') + attr('bold'), configuration_prompt[0]['message'],
                   fg('cyan') + attr('bold'), result[variable], attr('reset')))
        else:
            answers = PyInquirer_prompt(configuration_prompt, style=__ConfigurationsTheme)
            if not answers:
                raise KeyboardInterrupt
            result[variable] = str(answers[variable])

    # Footer
    print(' ', flush=True)

    # Result
    return result
