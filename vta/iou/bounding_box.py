"""Provides the BoundingBox class and related algorithms."""


class Point:
    """Encapsulates a Cartesian (x,y) point."""

    def __init__(self, x=0, y=0):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        """Get the Point's x coordinate."""
        return self.__x

    @property
    def y(self) -> int:
        """Get the Point's y coordinate."""
        return self.__y


class Size:
    """Encapsulates a size in two dimensions."""

    def __init__(self, width=0, height=0):
        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        """Get the size's width coordinate."""
        return self.__width

    @property
    def height(self) -> int:
        """Get the size's height coordinate."""
        return self.__height


class BoundingBox:
    """Defines a bounding box."""

    def __init__(self, upper_left_corner: Point, size: Size):
        self.__upper_left_corner = upper_left_corner
        self.__size = size
        self.__area = size.width * size.height

    @property
    def upper_left_corner(self) -> Point:
        """Get the location of the upper left corner of the bounding box."""
        return self.__upper_left_corner

    @property
    def size(self) -> Size:
        """Get the size of the bounding box."""
        return self.__size

    @property
    def area(self) -> int:
        """Get the area of the bounding box."""
        return self.__area


def calculate_iou(a: BoundingBox, b: BoundingBox) -> float:
    """Calculate the intersection-over-union of two bounding boxes.

    :param BoundingBox a: The first bounding box.
    :param BoundingBox b: The second Bounding box.
    :returns iou: The intersection-over-union value of ``a`` and ``b``.
    :rtype: float
    """
    return float(calculate_intersection(a, b)) / float(calculate_union(a, b))


def calculate_intersection(a: BoundingBox, b: BoundingBox) -> int:
    """Calculate the intersection of two bounding boxes.

    :param BoundingBox a: The first bounding box.
    :param BoundingBox b: The second Bounding box.
    :returns iou: The intersection of ``a`` and ``b``.
    :rtype: int
    """
    left = max(a.upper_left_corner.x, b.upper_left_corner.x)
    right = min(
        a.upper_left_corner.x + a.size.width, b.upper_left_corner.x + b.size.width
    )
    top = max(a.upper_left_corner.y, b.upper_left_corner.y)
    bottom = min(
        a.upper_left_corner.y + a.size.height, b.upper_left_corner.y + b.size.height
    )
    return max((bottom - top) * (right - left), 0)


def calculate_union(a: BoundingBox, b: BoundingBox) -> int:
    """Calculate the union of two bounding boxes.

    :param BoundingBox a: The first bounding box.
    :param BoundingBox b: The second Bounding box.
    :returns iou: The union of ``a`` and ``b``.
    :rtype: int
    """
    return a.area + b.area - calculate_intersection(a, b)
