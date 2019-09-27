"""The entry module for the vta loss command."""

import json
import os.path

import matplotlib.pyplot as plt
import numpy
import sklearn.linear_model


# TODO These constants need to be converted to command line or configuration
# parameters
LOSS_DIRECTORY = os.path.expanduser(
    "~/repositories/py-MDNet"
    # "~/repositories/phd/mdnet-data/control_loss_data/"
)


def main(arguments):
    """Runs the vta loss command.

    This is the main entry point for the VTA loss command. It will draw graphs
    of data related to machine learning loss during training.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta loss --help` for details.

    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    loss_data = _read_loss_data(arguments.file)
    if loss_data is list:
        _graph_loss_data(loss_data)
    elif arguments.domain is None:
        if "__all__" in loss_data:
            _graph_loss_data(loss_data["__all__"])
        else:
            print(
                "error: no domain specified, but no '__all__' domain available"
                " in the loss data."
            )
            return 1
    else:
        if "__all__" in loss_data:
            del loss_data["__all__"]
        domains = list(loss_data.keys())
        if len(domains) <= arguments.domain:
            print(
                "error: domain",
                arguments.domain,
                "was requested, but only",
                len(domains),
                "domains are available",
            )
            return 1
        _graph_domain_data(loss_data[domains[arguments.domain]])
    return 0


def make_parser(subparsers):
    """Creates an argument parser for the VTA loss command.

    :param subparsers: The subparsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The loss
        argument parser will be added to this.

    :return: Nothing
    """
    parser = subparsers.add_parser(
        "loss",
        help="Analyze data related to machine learning training loss.",
        prog="vta loss",
        description="This command can be used to draw graphs of data related to"
        " machine learning loss.",
    )
    parser.add_argument(
        "--domain",
        help="The particular domain to graph specified by number. If omitted,"
        " all loss data is graphed, without regard for domain. This option is"
        " ignored if the input data does not have domains.",
        type=int,
    )
    parser.add_argument(
        "file", help="The JSON file that has the loss data to graph."
    )


# -----------------------------------------------------------------------------
#                                                       implementation details
# -----------------------------------------------------------------------------
def _read_loss_data(file_path):
    with open(os.path.join(LOSS_DIRECTORY, file_path)) as loss_file:
        return json.load(loss_file)


def _graph_loss_data(data):
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure)

    # TODO Maybe draw a horizontal line at the loss minimum.
    # axes.axvline(score_threshold, alpha=0.5, color="r", label="Threshold")

    axes.scatter(range(len(data)), data, s=3, color="b")
    _graph_regression(axes, data)
    axes.legend()  # This must remain after the axes.plot() calls.
    plt.show()


def _make_axes(figure):
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Loss")
    axes.autoscale(enable=True, axis="both", tight=True)
    # axes.grid(
    #    b=True,
    #    which="major",
    #    axis="both",
    #    color="#101010",
    #    alpha=0.5,
    #    linestyle=":",
    # )
    return axes


def _graph_domain_data(domain_data):
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure)
    axes.set_title(domain_data["sequence"])
    axes.scatter(
        range(len(domain_data["loss"])), domain_data["loss"], s=3, color="b"
    )
    axes.legend()  # This must remain after the axes.plot() calls.
    plt.show()


def _graph_regression(axes, data):
    regression = sklearn.linear_model.LinearRegression()
    x = numpy.arange(len(data))  # pylint: disable=invalid-name
    regression.fit(x.reshape(-1, 1), numpy.array(data).reshape(-1, 1))
    prediction = regression.predict(x.reshape(-1, 1))
    axes.plot(x, prediction)
