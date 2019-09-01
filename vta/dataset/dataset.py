"""The entry module for the VTA dataset command."""

import os.path
import vta.utilities.file_utilities


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
        " the data set. If omitted, all sequences are downloaded.",
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
    print("Dataset", arguments.dataset, "is not yet implemented.")
    return 0
