"""The entry module for the vta scores command."""

import json
import os.path

import matplotlib.pyplot as plt


# TODO These constants need to be converted to command line or configuration
# parameters
SCORE_DIRECTORY = os.path.expanduser(
    os.path.join("~", "repositories", "py-MDNet")
)
FRAME = 0
SORT_SCORES = True


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
    _graph_score_data(score_data["frames"][FRAME])
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


def _graph_score_data(score_data):
    figure = plt.figure(figsize=(9, 6))
    axes = _make_axes(figure)
    _graph_data(axes, score_data["positive_scores"])
    plt.show()


def _make_axes(figure):
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title(f"Frame {FRAME} - Score Data")
    axes.autoscale(enable=True, axis="both", tight=True)
    axes.set_xlabel("Candidate")
    axes.set_ylabel("Raw Score")
    axes.grid(
        b=True,
        which="major",
        axis="both",
        color="#101010",
        alpha=0.5,
        linestyle=":",
    )
    return axes


def _graph_data(axes, data):
    axes.plot(
        range(len(data)),
        sorted(data) if SORT_SCORES else data,
        color="b",
        label="Sorted" if SORT_SCORES else "Unsorted",
        linewidth=1.0,
        linestyle="-",
        alpha=1.0,
    )
