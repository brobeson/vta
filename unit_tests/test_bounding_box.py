"""Unit tests for bounding box functionality."""

import unittest

import vta.iou.bounding_box as bounding_box


class BoundingBoxTest(unittest.TestCase):
    """Test cases for bounding box funcationality."""

    def test_box_area(self):
        """Validate calculation of a bounding box's area."""
        a = bounding_box.BoundingBox(bounding_box.Point(0, 0), bounding_box.Size(1, 1))
        self.assertEqual(a.area, 1)

        a = bounding_box.BoundingBox(
            bounding_box.Point(10, 10), bounding_box.Size(9, 8)
        )
        self.assertEqual(a.area, 72)

    def test_intersection(self):
        """Validate calculation of bounding box intersection."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(7, 5), bounding_box.Size(15, 20)
        )
        self.assertEqual(bounding_box.calculate_intersection(a, b), 45)

    def test_disjoint_intersection(self):
        """Validate that disjoint bounding boxes have 0 intersection."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(15, 5), bounding_box.Size(15, 20)
        )
        self.assertEqual(bounding_box.calculate_intersection(a, b), 0)

    def test_union(self):
        """Validate calculation of bounding box union."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(7, 5), bounding_box.Size(15, 20)
        )
        self.assertEqual(bounding_box.calculate_union(a, b), 355)

    def test_disjoint_union(self):
        """Validate calculation of the union of disjoint boxes."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(15, 5), bounding_box.Size(15, 20)
        )
        self.assertEqual(bounding_box.calculate_union(a, b), 400)

    def test_iou(self):
        """Validate calculation of bounding box IoU."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(7, 5), bounding_box.Size(15, 20)
        )
        self.assertAlmostEqual(bounding_box.calculate_iou(a, b), 0.12676056338)

    def test_disjoint_iou(self):
        """Validate calculation of the IoU of disjoint boxes."""
        a = bounding_box.BoundingBox(
            bounding_box.Point(5, 10), bounding_box.Size(5, 20)
        )
        b = bounding_box.BoundingBox(
            bounding_box.Point(15, 5), bounding_box.Size(15, 20)
        )
        self.assertAlmostEqual(bounding_box.calculate_iou(a, b), 0.0)
