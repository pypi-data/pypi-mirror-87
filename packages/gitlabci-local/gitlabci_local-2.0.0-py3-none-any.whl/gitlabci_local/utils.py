#!/usr/bin/env python3

# Libraries
from pathlib import Path, PurePosixPath
import re
import regex

# Components
from .const import Platform

# Dictionnaries getter
def dictGet(data, path):

    # Variables
    queries = path.split('.')
    result = None

    # Iterate through queries
    for query in queries:

        # Parse query to key and index
        parse = regex.match(r'([^\[]*)(\[(\d)\])*', query)
        if parse.group(1) and parse.captures(3):
            key = parse.group(1)
            indexes = [int(value) for value in parse.captures(3)]
        else:
            key = query
            indexes = []

        # Extract key
        if key:
            if result:
                if isinstance(result, list):
                    result = [value.get(key, None) if value else None for value in result]
                else:
                    result = result.get(key, None)
            else:
                result = data.get(key, None)

        # Extract index
        for index in indexes:
            if result and result[index]:
                result = result[index]
            else:
                result = None

        # Empty node
        if not result:
            break

    # Result
    return result

# Name checker
def nameCheck(name, items, no_regex):

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
                if re.search(item, re.escape(name)):
                    return True
            except:
                pass

    # Result
    return False

# Path getter
def getPath(path):

    # POSIX path
    path = PurePosixPath(path)

    # Result
    return str(path)

# Path resolver
def resolvePath(path):

    # Resolve path
    path = Path(path).resolve()

    # Linux path
    if Platform.IS_LINUX:
        path = str(path)

    # Windows path
    elif Platform.IS_WINDOWS:
        path = str(path)

    # Result
    return path
