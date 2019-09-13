"""The entry module for the vta scores command."""

import json
import os.path
import pdb

import matplotlib.pyplot as plt
import numpy


# TODO These constants need to be converted to command line or configuration
# parameters
SCORE_DIRECTORY = os.path.expanduser(
    os.path.join("~", "repositories", "py-MDNet")
)
FRAME = 0
SORT_SCORES = False


def main(arguments):
    """Runs the vta scores command.

    This is the main entry point for the VTA scores command. It will draw graphs
    of data related to machine learning output scores.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta scores --help` for details.

    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    score_data = _read_score_data(arguments.sequence)
    _graph_score_data(
        score_data["score_threshold"],
        score_data["frames"][FRAME],
        arguments.sequence,
    )
    return 0


def make_parser(subparsers):
    """Creates an argument parser for the VTA scores command.

    :param subparsers: The subparsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The scores
        argument parser will be added to this.

    :return: Nothing
    """
    parser = subparsers.add_parser(
        "scores",
        help="Analyze data related to machine learning output scores.",
        prog="vta scores",
        description="This command can be used to draw graphs of data related to"
        " machine learning scores. The scores are understood to be the raw"
        " output of the machine learning algorithm or model during tracking.",
    )
    parser.add_argument(
        "sequence", help="The sequence for which to load score data."
    )


# -----------------------------------------------------------------------------
#                                                       implementation details
# -----------------------------------------------------------------------------
def _read_score_data(sequence):
    filename = os.path.join(SCORE_DIRECTORY, f"{sequence}.json")
    with open(filename) as json_file:
        score_data = json.load(json_file)
    return score_data


def _graph_score_data(score_threshold, frame_data, sequence):
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure, sequence)
    distance_data = _make_distance_stats(frame_data)
    # _graph_data(axes, frame_data["positive_scores"], distance_data)

    axes.axvline(score_threshold, alpha=0.5, color="r", label="Threshold")

    frame_data["positive_scores"] = numpy.array(frame_data["positive_scores"])
    _scatter_data(
        axes,
        frame_data["positive_scores"],
        distance_data,
        "b",
        label="Candidates",
    )

    # Draw the data for the top indices
    frame_data["top_indices"] = numpy.array(frame_data["top_indices"])
    _scatter_data(
        axes,
        frame_data["positive_scores"][frame_data["top_indices"]],
        distance_data[frame_data["top_indices"]],
        "r",
        label="Top Scores",
    )

    # _graph_top_indices(axes,
    axes.legend()  # This must remain after the axes.plot() calls.
    plt.show()


def _make_axes(figure, sequence):
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(f"{sequence} - Frame {FRAME}")
    axes.autoscale(enable=True, axis="both", tight=True)
    axes.grid(
        b=True,
        which="major",
        axis="both",
        color="#101010",
        alpha=0.5,
        linestyle=":",
    )
    return axes


def _scatter_data(axes, x_data, y_data, color, label):
    axes.scatter(x_data, y_data, s=3, color=color, label=label)
    axes.set_xlabel("Candidate Scores")
    axes.set_ylabel("Distance from Previous Target (pixels)")


def _graph_data(axes, x_data, y_data):
    axes.plot(
        x_data,
        sorted(y_data) if SORT_SCORES else y_data,
        color="b",
        label="Sorted" if SORT_SCORES else "Unsorted",
        linewidth=1.0,
        linestyle="-",
        alpha=1.0,
    )
    axes.set_xlabel("Candidate")
    axes.set_ylabel("Raw Score")


def _graph_top_indices(axes, x_data, y_data):
    axes.scatter(x_data, y_data, s=4, color="r")


def _make_distance_stats(frame_data):
    target = numpy.array(frame_data["target"])
    candidates = numpy.array(frame_data["samples"])
    # TODO Use numpy routines; they're probably faster.
    differences = target[0:2] - candidates[:, 0:2]
    differences = differences ** 2
    differences = numpy.sum(differences, axis=1)
    distances = numpy.sqrt(differences)
    return distances
