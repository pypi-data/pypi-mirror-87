#!/usr/bin/env python3

# Components
from ..system.platform import Platform
from .colors import Colors

# Boxes class
class Boxes:

    # Constants
    __TOP_LEFT = '╭'
    __TOP_LINE = '─'
    __TOP_RIGHT = '╮'
    __MIDDLE_LEFT = '│'
    __MIDDLE_RIGHT = '│'
    __BOTTOM_LEFT = '╰'
    __BOTTOM_LINE = '─'
    __BOTTOM_RIGHT = '╯'
    __OFFSET_LINE = '   '
    __PADDING_LINE = 3

    # Members
    __lines = None

    # Constructor
    def __init__(self):
        self.__lines = []

    # Adder
    def add(self, line):
        self.__lines += [line]

    # Printer
    def print(self):

        # Variables
        length = 0

        # Evaluate lines length
        length = max(len(Colors.strip(line)) for line in self.__lines)

        # Add lines padding
        length += 2 * Boxes.__PADDING_LINE

        # Header
        print(' ')

        # Print header line
        print('%s%s%s%s%s' % (Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__TOP_LEFT,
                              Boxes.__TOP_LINE * length, Boxes.__TOP_RIGHT))

        # Print content lines
        for line in self.__lines:
            print('%s%s%s%s%s%s' %
                  (Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__MIDDLE_LEFT,
                   Colors.center(line, length), Colors.YELLOW, Boxes.__MIDDLE_RIGHT))

        # Print bottom line
        print('%s%s%s%s%s' % (Boxes.__OFFSET_LINE, Colors.YELLOW, Boxes.__BOTTOM_LEFT,
                              Boxes.__BOTTOM_LINE * length, Boxes.__BOTTOM_RIGHT))

        # Footer
        print(' ')
        Platform.flush()
