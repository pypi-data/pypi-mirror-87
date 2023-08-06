# -*- coding: utf-8 -*-

"""Some helperfunctions for clis."""

import sys

from termcolor import cprint

VERBOSITY = 5
DEBUG_PRINT_LEVELS = [
    {"color": "blue", "attrs": ["bold"]},
    {"color": "blue", "attrs": []},
    {"color": "white", "attrs": ["bold"]},
    {"color": "white", "attrs": []},
    {"color": "grey", "attrs": []},
    {"color": "grey", "attrs": ["dark"]},
]


def set_verbosity(verbosity):
    """sets the verbosity level of this script"""
    global VERBOSITY
    VERBOSITY = verbosity


def error(message):
    """prints the message to stderr and exits"""
    cprint(f"[!] {message}", attrs=["bold"], color="red", file=sys.stderr)
    sys.exit(1)


def debug(message, min_debug_level):
    """prints the message to stdout if debug level >= min_debug_level"""
    if min_debug_level <= VERBOSITY:
        cprint(
            f"[i] {message}",
            color=DEBUG_PRINT_LEVELS[min_debug_level]["color"],
            attrs=DEBUG_PRINT_LEVELS[min_debug_level]["attrs"],
        )
