"""Functions and classes for working with files."""

import os.path
import sys


# The PyLint suppressions are necessary. This class implements the
# argparse.Action interface, so it must be this way.
class DirectoryValidator:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Validates that a command argument represents a legitimate directory.

    This is intended for use with
    :py:func:`argparse.ArgumentParser.add_argument` when adding a directory
    argument. Pass this as the ``action`` parameter. It will ensure that the
    value entered for the command line argument either a) does not exist, or b)
    exists and is a directory. This ensures that when a directory is required,
    there will not be a conflict with something that is *not* a directory.

    .. code-block:: python

        import argparse
        from vta.utilities.file_utilities import DirectoryValidator

        parser = argparse.ArgumentParser("print")
        parser.add_argument("--out-dir", action=DirectoryValidator)
        parser.parse_args()

    If ``print`` is then invoked with path to a regular file, the
    :py:class:`DirectoryValidator` will exit the program with an error message.

    .. code-block:: none

        $ print --out-dir=~/.bashrc
        error: /home/me/.bashrc already exists and is not a directory

    """

    # #lizard forgives
    def __init__(  # pylint: disable=too-many-arguments
        self,
        option_strings,
        dest,
        nargs=None,
        const=None,
        default=None,
        type=None,  # pylint: disable=redefined-builtin
        choices=None,
        required=False,
        help=None,  # pylint: disable=redefined-builtin
        metavar=None,
    ):
        self.option_strings = option_strings
        self.dest = dest
        self.nargs = nargs
        self.const = const
        self.default = default
        self.type = type
        self.choices = choices
        self.required = required
        self.help = help
        self.metavar = metavar

    def __call__(self, parser, namespace, values, option_string):
        directory = os.path.abspath(os.path.expanduser(values))
        if os.path.exists(directory) and not os.path.isdir(directory):
            sys.exit(f"error: {directory} already exists and is not a directory")
        setattr(namespace, option_string, directory)
