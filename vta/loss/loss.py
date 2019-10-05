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
    configuration = _augment_configuration(configuration["loss"])
    labels, losses, precisions = _read_loss_data(arguments.file)
    #losses = _limit_data(
    #    losses, "loss", configuration["maximum_graphs"], configuration["whats_best"]
    #)
    #precisions = _limit_data(
    #    precisions,
    #    "precision",
    #    configuration["maximum_graphs"],
    #    configuration["whats_best"],
    #)
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure)
    if configuration["draw_loss"]:
        for label, loss in zip(labels, losses):
            axes.plot(
                range(len(loss)),
                loss,
                label=label,
                linestyle="-" if configuration["line_loss"] else "",
                marker="." if configuration["scatter_loss"] else "",
            )
    if configuration["draw_precision"]:
        for label, precision in zip(labels, precisions):
            axes.plot(
                range(len(precision)),
                precision,
                label=label,
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
    parser.add_argument(
        "file", help="The JSON file that has the loss data to graph.", nargs="+"
    )


# -----------------------------------------------------------------------------
#                                                       implementation details
# -----------------------------------------------------------------------------
def _augment_configuration(configuration):
    configuration["draw_loss"] = (
        configuration["scatter_loss"] or configuration["line_loss"]
    )
    configuration["draw_precision"] = (
        configuration["scatter_precision"] or configuration["line_precision"]
    )
    #configuration["whats_best"] = configuration["whats_best"].lower()
    return configuration


def _read_loss_data(file_paths):
    labels = []
    losses = []
    precisions = []
    for file_path in file_paths:
        with open(os.path.join(file_path)) as loss_file:
            data = json.load(loss_file)
        if "label" in data:
            labels.append(data["label"])
        else:
            labels.append(file_path)
        losses.append(numpy.array(data["loss"]))
        precisions.append(numpy.array(data["precision"]))
    return labels, losses, precisions


#def _limit_data(data, data_type, limit, algorithm):
#    if len(data) <= limit:
#        return data
#    criteria = numpy.fromiter((d.mean() for d in data), dtype=float)
#    data = numpy.array(data)
#    return data


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


def _graph_regression(axes, data):
    """
    .. todo:: See issue #7
    """
    regression = sklearn.linear_model.LinearRegression()
    x_data = numpy.arange(len(data))  # pylint: disable=invalid-name
    regression.fit(x_data.reshape(-1, 1), numpy.array(data).reshape(-1, 1))
    # x_data = numpy.arange(0.0, len(data), 0.1)
    x_data = numpy.linspace(0.0, len(data), 100)
    prediction = regression.predict(x_data.reshape(-1, 1))
    axes.plot(x_data, prediction)


def _graph_fit(axes, data):
    """
    .. todo:: See issue #7
    """
    interpolation = scipy.interpolate.interp1d(range(len(data)), data)
    x_data = numpy.linspace(0, len(data), 100)
    axes.plot(x_data, interpolation(x_data))
