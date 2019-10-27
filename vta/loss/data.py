"""Provides data structures for encapsulating loss data."""

import numpy


class Loss:
    """Encapsulates training loss data.

    .. py:attribute:: label
        A string that will be used in graph legends for this loss data.

    .. py:attribute:: loss_values
        A numpy.ndarray containing the training loss data.

    .. py:attribute:: precision_values
        A numpy.ndarray containing the training precision data.
    """

    def __init__(
        self, label: str, loss_values: numpy.ndarray, precision_values: numpy.ndarray
    ):
        self.label = label
        self.loss_values = loss_values
        self.precision_values = precision_values


LossList = list


def has_invalid_values(loss: Loss) -> bool:
    """Determine if loss or precision data has invalid values.

    :param data: The loss or precision data to check for invalid values. This
        should be a Loss or Precision object.
    :returns: True is returned if data has at least one invalid value. False is
        returned if all values in data are valid.
    :rtype: bool

    This function will tell you if the data has any values that are NaN,
    +infinity, or -infinity.
    """
    return numpy.any(numpy.logical_not(numpy.isfinite(loss.loss_values))) or numpy.any(
        numpy.logical_not(numpy.isfinite(loss.precision_values))
    )


def sort_by_loss(losses: LossList, algorithm: str) -> None:
    """Sort the loss data according to the specified algorithm.

    :param LossList losses: The list of loss data to sort. This list is sorted
        in place.
    :param str algorithm: The algorithm to use for sorting. See the loss
        configuration item ``sort_algorithm`` for acceptable values.
    :returns: None

    This function sorts the loss data, based on loss values (not precision
    values). The list is sorted from best to worst. For loss, best is always the
    lowest. The list below defines what is compared to determine what is lowest.
    For the examples described below, assume two sets of loss data, with the
    given values:

    .. code-block::

        baseline = [ 5, 2, 1, 2 ]
        new_loss = [ 4, 3, 2, 1 ]

    :last: Comparisons are made between the last value in each list of loss
        data. Using this algorithm for the example data, ``new_loss`` will be
        sorted ahead of ``baseline``. ``baseline[4]`` is 2, while
        ``new_loss[4]`` is 1.
    """
    if algorithm == "last":
        losses.sort(key=lambda l: l.loss_values[-1])


def sort_by_precision(losses: LossList, algorithm: str) -> None:
    """Sort the loss data according to the specified algorithm.

    :param LossList losses: The list of loss data to sort. This list is sorted
        in place.
    :param str algorithm: The algorithm to use for sorting. See the loss
        configuration item ``sort_algorithm`` for acceptable values.
    :returns: None

    This function sorts the loss data, based on precision values (not loss
    values). The list is sorted from best to worst. For precision, best is
    always the highest. The list below defines what is compared to determine
    what is highest. For the examples described below, assume two sets of
    precision data, with the given values:

    .. code-block::

        baseline = [ 5, 2, 1, 2 ]
        new_loss = [ 4, 3, 2, 1 ]

    :last: Comparisons are made between the last value in each list of loss
        data. Using this algorithm for the example data, ``baseline`` will be
        sorted ahead of ``new_loss``. ``baseline[4]`` is 2, while
        ``new_loss[4]`` is 1.
    """
    if algorithm == "last":
        losses.sort(key=lambda l: l.precision_values[-1], reverse=True)
