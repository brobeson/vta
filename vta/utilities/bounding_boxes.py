"""
vta.utilities.bounding_boxes
============================

Classes and functions for interacting with bounding boxes.
"""

import numpy


class BoundingBoxList:
    """
    A list of axis aligned bounding boxes.
    """

    def __init__(self, boxes: numpy.ndarray):
        """
        Initialize a list of bounding boxes.

        :param numpy.ndarray boxes: The data for the bounding boxes. This must be a 2D array with
            shape (N,4). Each row is interpreted as one bounding box. Each box is interpreted as
            [x, y, width, height].
        """
        self.boxes = boxes

    @property
    def coordinates(self):
        """An (N,2) array of the [X,Y] coordinates of the boxes."""
        return self.boxes[:, :2]

    def dimensions(self):
        return self.boxes[:, 2:]
