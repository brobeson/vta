"""The entry module for the vta loss command."""

import json

import matplotlib.pyplot as plt
import numpy
import scipy.interpolate
import sklearn.linear_model

import vta.loss.data


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
    losses = _read_loss_data(arguments.file)
    if configuration["reject_invalid_data"]:
        losses = [l for l in losses if _filter_invalid_data(l)]
    figure = plt.figure(figsize=(15, 10))
    axes = _make_axes(figure, configuration)
    _graph_loss(configuration, axes, losses)
    _graph_precision(configuration, axes, losses)
    axes.legend()  # This must remain after the data is graphed.
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
def _filter_invalid_data(data):
    if vta.loss.data.has_invalid_values(data):
        print("warning:", data.label, "has invalid data")
        return False
    return True


def _graph_loss(configuration, axes, losses):
    if not configuration["draw_loss"]:
        return
    vta.loss.data.sort_by_loss(losses, configuration["sort_algorithm"])
    for loss in losses[0:configuration["maximum_graphs"]]:
        value = loss.loss_values[-1]
        axes.plot(
            range(len(loss.loss_values)),
            loss.loss_values,
            label=f"[{value:.3f}] {loss.label}",
            linestyle="-" if configuration["line_loss"] else "",
            marker="." if configuration["scatter_loss"] else "",
        )


def _graph_precision(configuration, axes, precisions):
    if not configuration["draw_precision"]:
        return
    vta.loss.data.sort_by_precision(precisions, configuration["sort_algorithm"])
    for precision in precisions[0:configuration["maximum_graphs"]]:
        value = precision.precision_values[-1]
        axes.plot(
            range(len(precision.precision_values)),
            precision.precision_values,
            label=f"[{value:.3f}] {precision.label}",
            linestyle="-" if configuration["line_precision"] else "",
            marker="." if configuration["scatter_precision"] else "",
        )


def _augment_configuration(configuration):
    configuration["draw_loss"] = (
        configuration["scatter_loss"] or configuration["line_loss"]
    )
    configuration["draw_precision"] = (
        configuration["scatter_precision"] or configuration["line_precision"]
    )
    # configuration["sort_algorithm"] = configuration["sort_algorithm"].lower()
    return configuration


def _read_loss_data(file_paths):
    losses = vta.loss.data.LossList()
    for file_path in file_paths:
        with open(file_path) as loss_file:
            data = json.load(loss_file)
        losses.append(
            vta.loss.data.Loss(
                data["label"] if "label" in data else file_path,
                numpy.array(data["loss"]),
                numpy.array(data["precision"]),
            )
        )
    return losses


def _has_invalid_values(data):
    return numpy.any(numpy.logical_not(numpy.isfinite(data)))


# def _limit_data(data, data_type, limit, algorithm):
#    if len(data) <= limit:
#        return data
#    #if data_type == "loss":
#    #    return _limit_loss_data(data, limit, algorithm)
#    #if data_type == "precision":
#    #    return _limit_precision_data(data, limit, algorithm)
#    #criteria = numpy.fromiter((d.mean() for d in data), dtype=float)
#    #data = numpy.array(data)
#    #return data
#    #sys.exit(f"error: '{algorithm}' is not a valid method for limiting data")


# def _limit_loss_data(data, limit, algorithm):
#    if algorithm == "last":


def _make_axes(figure, configuration):
    axes = figure.add_subplot(1, 1, 1)
    if configuration["draw_loss"] and configuration["draw_precision"]:
        axes.set_title("Loss and Precision")
    elif configuration["draw_loss"]:
        axes.set_title("Loss")
    elif configuration["draw_precision"]:
        axes.set_title("Precision")
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
