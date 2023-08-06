#!/usr/bin/env python3

# Standard libraries
from re import escape, search

# Lists class
class Lists:

    # Match
    @staticmethod
    def match(items, name, no_regex):

        # Search without regex
        if name in items:
            return True

        # Search with regex
        if not no_regex:
            for item in items:

                # Search with string inclusion
                if item in name:
                    return True

                # Search with real regex
                try:
                    if search(item, escape(name)):
                        return True
                except:
                    pass

        # Result
        return False
