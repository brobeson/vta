"""The entry module for the vta iou command."""

import argparse
import glob


def main(arguments):
    """Runs the vta iou command.

    This is the main entry point for the VTA iou command. It will draw graphs
    of data related to machine learning intersection-over-union results.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta iou --help` for details.
    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    files = glob.glob(f"{arguments.results_directory}/*json")



def make_parser(subparsers, common_options):
    """Creates an argument parser for the VTA iou command.

    :param subparsers: The subparsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The iou argument parser will be added to
        this.
    :param common_options:

    :return: Nothing
    """
    parser = subparsers.add_parser(
        "iou",
        help="Analyze intersection-over-union results.",
        prog="vta iou",
        description="This command can be used to draw graphs of IoU tracking results.",
        parents=[common_options],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "results_directory", help="The directory with JSON bounding box data."
    )
