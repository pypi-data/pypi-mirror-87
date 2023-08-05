#!/usr/bin/env python3

# Libraries
import copy
import oyaml as yaml

# Components
from .utils import nameCheck

# Dumper
def dumper(options, jobs):

    # Variables
    configuration = dict()
    result = False

    # Prepare configuration results
    if options.names:
        for job in jobs:
            if nameCheck(job, options.names, options.no_regex):
                configuration[job] = copy.deepcopy(jobs[job])
                del configuration[job]['options']
                result = True
    else:
        for job in jobs:
            configuration[job] = copy.deepcopy(jobs[job])
            del configuration[job]['options']
        result = True

    # Dump configuration results
    print(yaml.dump(configuration, indent=2))
    print(' ', flush=True)

    # Result
    return result
