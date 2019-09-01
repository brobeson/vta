"""The entry module for the VTA dataset command."""

import os.path
import sys
import vta.dataset.vot
import vta.utilities.file_utilities


SUBSETS = {
    "otb": ["tb50", "tb100"],
    "vot": ["2013", "2014", "2015", "2016", "2017"],
}


# The PyLint suppressions are necessary. This class implements the
# argparse.Action interface, so it must be this way.
class SubsetLister:  # pylint: disable=too-many-instance-attributes,too-few-public-methods
    """Validates that a command argument represents a legitimate directory."""

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
        for subset in SUBSETS[namespace.dataset]:
            print(subset)
        sys.exit(0)


def make_parser(subparsers):
    """Creates an argument parser for the VTA dataset command.

    Args:
        subparsers: The subparsers object returned by a call to
            argparse.ArgumentParser.add_subparsers(). The dataset argument
            parser will be added to this.

    Returns:
        Nothing

    Raises:
        Nothing: This function should not raise any exceptions. If you encounter
            one, please file a bug issue.
    """
    parser = subparsers.add_parser(
        "dataset",
        help="Download a video data set, or part of a data set.",
        prog="vta dataset",
        description="This command can be used to download common data sets used"
        " in visual tracking research. It can also be used to download"
        " individual sequences from those data sets.",
    )
    parser.add_argument(
        "dataset",
        choices=["otb", "vot"],
        help="The data set to download, or from which to download sequences.",
    )
    parser.add_argument(
        "subsets",
        choices=["2013", "2014", "2015", "2016", "2017", "tb50", "tb100"],
        help="An optional subset of the dataset to download. If omitted, the"
        " full data set is downloaded. Note that not all subsets are available"
        " for all data sets. For example, tb50 does not exist in the VOT data"
        " set. If incompatible data set and subset are specified, an error will"
        " be printed and nothing will be downloaded. Use 'vta dataset {set}"
        " --list-subsets' to view subsets available for a particular data set.",
        nargs="+",
    )
    parser.add_argument(
        "--list-subsets",
        help="Show the subsets that are valid for the specified subset.",
        action=SubsetLister,
        nargs=0,
    )
    default_root = os.path.expanduser("~/Videos")
    parser.add_argument(
        "--root-directory",
        help="The root directory in which to download the data. A subdirectory"
        " will be created that matches the name of the data set. For example,"
        " if you specify 'otb --root-directory=~/Videos', the directory"
        " '~/Vidoes/otb' will be created. The default is " + default_root + ".",
        action=vta.utilities.file_utilities.DirectoryValidator,
        default=default_root,
        metavar="DIR",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If present, download requested data even if it is already"
        " present.",
    )
    parser.add_argument(
        "--sequences",
        nargs="+",
        help="A space separated list of individual sequences to download from"
        " the data set. If omitted, all sequences from the specified data set"
        " and subset are downloaded. If a sequence is not in the data set and"
        " subset, an error is printed to the console, but downloading will"
        " continue.",
        metavar="SEQUENCE",
    )


def main(arguments):
    """Runs the vta dataset command.

    This is the main entry point for the VTA dataset command. It will attempt to
    download a dataset, or specific sequences, according to the supplied
    arguments.

    Args:
        arguments: The command line arguments, as parsed by the argparse module.
        Run 'vta dataset --help' for details.

    Returns:
        An integer exit code following Unix command conventions. 0 indicates
        that command processing succeeded. Any other value indicates that an
        error occurred.

    Raises:
        Nothing
    """
    _print_summary(arguments)
    if arguments.dataset == "vot":
        return vta.dataset.vot.download_sequences(
            arguments.subsets,
            arguments.root_directory,
            arguments.force,
            arguments.sequences,
        )
    print("Dataset", arguments.dataset, "is not yet implemented.")
    return 1


#------------------------------------------------------------------------------
#                                                       implementation details
#------------------------------------------------------------------------------
def _print_summary(arguments):
    print("Downloading ", end="")
    if arguments.subsets is None:
        print("all subsets ", end="")
    else:
        print("subsets", ", ".join(arguments.subsets), "", end="")
    print(f"from {arguments.dataset}.")
    if arguments.sequences is None:
        print("Downloading all sequences.")
    else:
        print("Downloading these sequences.")
        for sequence in arguments.sequences:
            print("  ", sequence)
    if arguments.force:
        print("Downloading sequences that already exist.")
    else:
        print("Skipping sequences that already exist.")
    print(f"Downloading to {arguments.root_directory}.")
