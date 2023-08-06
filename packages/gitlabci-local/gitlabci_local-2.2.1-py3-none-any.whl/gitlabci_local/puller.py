#!/usr/bin/env python3

# Components
from .engines.engine import Engine

# Puller
def puller(options, jobs):

    # Variables
    images = []
    result = False

    # List container images
    for job in jobs:
        image = jobs[job]['image']
        if image and not jobs[job]['options']['host'] and image not in images:
            images += [image]
            result = True

    # Create container engine
    engine = Engine(options)

    # Pull container images
    if images:
        images.sort()
        for image in images:
            engine.pull(image)

    # Result
    return result
