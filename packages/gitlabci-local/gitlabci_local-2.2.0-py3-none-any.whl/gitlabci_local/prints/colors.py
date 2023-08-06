#!/usr/bin/env python3

# Modules libraries
from colored import attr, fg

# Colors class
class Colors:

    # Constants
    BOLD = attr('reset') + attr('bold')
    CYAN = fg('cyan') + attr('bold')
    GREEN = fg('green') + attr('bold')
    GREY = fg('light_gray') + attr('bold')
    RED = fg('red') + attr('bold')
    RESET = attr('reset')
    YELLOW = fg('yellow') + attr('bold')
    YELLOW_LIGHT = fg('light_yellow') + attr('bold')

    # Attributes
    __ALL = [BOLD, CYAN, GREEN, GREY, RED, RESET, YELLOW, YELLOW_LIGHT]

    # Center
    @staticmethod
    def center(string, length):

        # Extract text
        text = Colors.strip(string)

        # Center string
        if len(text) < length:
            paddings = length - len(text)
            left = paddings // 2
            right = -(-paddings // 2)
            return ' ' * left + string + ' ' * right

        # Default string
        return string

    # Strip
    @staticmethod
    def strip(string):
        for item in Colors.__ALL:
            string = string.replace(item, '')
        return string
