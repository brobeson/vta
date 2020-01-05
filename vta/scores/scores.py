"""The entry module for the vta scores command."""

import argparse
import json

import vta.utilities.console as console


def main(arguments):
    """Runs the vta scores command.

    This is the main entry point for the VTA scores command. It will draw graphs of data related to
    machine learning scores, or network output.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta scores --help` for details.
    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    score_data = _read_score_data(arguments.score_file)
    _validate_score_data(score_data)
    if not score_data:
        console.print_error("No score data to graph.")
        return 1
    return 0


def make_parser(subparsers):
    """Creates an argument parser for the VTA scores command.

    :param subparsers: The subparsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The loss argument parser will be added to
        this.
    :return: Nothing
    """
    parser = subparsers.add_parser(
        "scores",
        help="Analyze data related to machine learning output scores.",
        prog="vta loss",
        description="This command can be used to draw graphs of data related to machine learning"
        "scores.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "score_file", help="The JSON file that has the score data to graph."
    )


# -----------------------------------------------------------------------------
#                                                       implementation details
# -----------------------------------------------------------------------------
def _read_score_data(score_file):
    with open(score_file) as f:
        return json.load(f)


def _validate_score_data(score_data):
    indices_to_delete = set()
    for i, frame in enumerate(score_data):
        if len(frame["negative_boxes"]) != len(frame["negative_scores"]):
            console.print_warning(
                f"Frame {frame['frame']}: {len(frame['negative_boxes'])} negative"
                f" bounding boxes and {len(frame['negative_scores'])} scores"
            )
            indices_to_delete.add(i)
        if len(frame["positive_boxes"]) != len(frame["positive_scores"]):
            console.print_warning(
                f"Frame {frame['frame']}: {len(frame['positive_boxes'])} positive"
                f" bounding boxes and {len(frame['positive_scores'])} scores"
            )
            indices_to_delete.add(i)
    indices_to_delete = list(indices_to_delete)
    indices_to_delete.sort(reverse=True)
    for i in indices_to_delete:
        del score_data[i]
