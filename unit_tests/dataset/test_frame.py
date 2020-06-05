"""Unit test for the Frame class."""

import unittest

from vta.dataset.dataset_class import Frame

class FrameTest(unittest.TestCase):
    """Test cases for the Frame class."""

    def test_initialization(self):
        frame = Frame(1, [0, 0, 10, 10], None)
        self.assertEqual(frame.index, 1)
        self.assertEqual(frame.ground_truth)
