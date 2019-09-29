"""The entry module for the vta loss command."""

import json
import os.path

import matplotlib.pyplot as plt
import numpy
import scipy.interpolate
import sklearn.linear_model


def main(arguments, configuration):
    """Runs the vta loss command.

    This is the main entry point for the VTA loss command. It will draw graphs
    of data related to machine learning loss during training.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta loss --help` for details.
    :param dict configuration: An optional run time configuration. In normal
        use, this will have been read from a YAML file.
    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    configuration = configuration["loss"]
    loss, precision = _read_loss_data(arguments.file)
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure)
    axes.plot(
        range(len(loss)),
        loss,
        label="Loss",
        linestyle="-" if configuration["line_loss"] else "",
        marker="." if configuration["scatter_loss"] else "",
    )
    axes.plot(
        range(len(precision)),
        precision,
        label="Precision",
        linestyle="-" if configuration["line_precision"] else "",
        marker="." if configuration["scatter_precision"] else "",
    )
    axes.legend()  # This must remain after the axes.plot() calls.
    plt.show()


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
    parser.add_argument("file", help="The JSON file that has the loss data to graph.")


# -----------------------------------------------------------------------------
#                                                       implementation details
# -----------------------------------------------------------------------------
def _read_loss_data(file_path):
    with open(os.path.join(file_path)) as loss_file:
        data = json.load(loss_file)
    return numpy.array(data["loss"]), numpy.array(data["precision"])


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


# TODO Need to get a good curve fit to the data. See issue #7.

#def _graph_regression(axes, data):
#    regression = sklearn.linear_model.LinearRegression()
#    x = numpy.arange(len(data))  # pylint: disable=invalid-name
#    regression.fit(x.reshape(-1, 1), numpy.array(data).reshape(-1, 1))
#    #x = numpy.arange(0.0, len(data), 0.1)
#    x = numpy.linspace(0.0, len(data), 100)
#    prediction = regression.predict(x.reshape(-1, 1))
#    axes.plot(x, prediction)


#def _graph_fit(axes, data):
#    interpolation = scipy.interpolate.interp1d(range(len(data)), data)
#    x = numpy.linspace(0, len(data), 100)
#    axes.plot(x, interpolation(x))
