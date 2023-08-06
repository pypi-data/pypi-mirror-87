#!/usr/bin/env python3

# Standard libraries
from copy import deepcopy
from oyaml import dump as yaml_dump

# Components
from .types.lists import Lists

# Dumper
def dumper(options, jobs):

    # Variables
    configuration = dict()
    result = False

    # Prepare configuration results
    if options.names:
        for job in jobs:
            if Lists.match(options.names, job, options.no_regex):
                configuration[job] = deepcopy(jobs[job])
                del configuration[job]['options']
                result = True
    else:
        for job in jobs:
            configuration[job] = deepcopy(jobs[job])
            del configuration[job]['options']
        result = True

    # Dump configuration results
    print(yaml_dump(configuration, indent=2))
    print(' ', flush=True)

    # Result
    return result
