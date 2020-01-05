"""Functions for interacting on the console."""

import textwrap

INDENT = "           "
WRAPPER = textwrap.TextWrapper(width=80-len(INDENT) - 1)

def print_error(message: str):
    """Print an error to the console."""
    lines = WRAPPER.wrap(message)
    print("[", "\033[01;31merror\033[0m", "  ]", message)
    del lines[0]
    for l in lines:
        print(INDENT, l)


def print_warning(message: str):
    """Print an warning to the console."""
    lines = WRAPPER.wrap(message)
    print("[", "\033[01;33mwarning\033[0m", "]", lines[0])
    del lines[0]
    for l in lines:
        print(INDENT, l)
