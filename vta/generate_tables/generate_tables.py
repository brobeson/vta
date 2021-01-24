"""The entry module for the vta tables command."""

import argparse
import glob
import os.path


def main(arguments):
    # TODO I'm looking for the wrong informatin in the wrong spot.
    arguments.results_path = os.path.abspath(os.path.expanduser(arguments.results_path))
    print("Scanning results in", arguments.results_path)
    trackers = _get_trackers(arguments.results_path)
    print("Found trackers:")
    for tracker in trackers:
        print(" ", tracker)
    return 0


def make_parser(subparsers, common_options):
    parser = subparsers.add_parser(
        "tables",
        help="Genreate LaTeX tables summarizing tracking results.",
        prog="vta tables",
        description="This command can be used to summarize tracking results in LaTeX tables.",
        parents=[common_options],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "results_path", help="The path to the tracking results to summarize."
    )


def _get_trackers(results_path: str) -> list:
    """
    Get the list of trackers in the results path.

    :param str results_path: The root path to the results.
    :return: A list of strings representing each tracker in the results.
    :rtype: list
    """
    trackers = glob.glob(os.path.join(results_path, "*"))
    trackers = [os.path.basename(f) for f in trackers if os.path.isdir(results_path)]
    trackers.sort()
    return trackers
