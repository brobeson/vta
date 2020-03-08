"""Classes and functions related to an image sequence."""

import os.path
import PIL.Image
import PIL.ImageDraw


class Point:
    """Represents a point location in an image."""

    def __init__(self, x: int, y: int):
        self.__x = int(x)
        self.__y = int(y)

    @property
    def x(self) -> int:
        """Get the point's X coordinate."""
        return self.__x

    @property
    def y(self) -> int:
        """Get the point's Y coordinate."""
        return self.__y

    def __mul__(self, scale_factor):
        return Point(self.x * scale_factor, self.y * scale_factor)


class Dimensions:
    """Represents dimensions within an image."""

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        """Get the width dimension."""
        return self.__width

    @property
    def height(self) -> int:
        """Get the height dimension."""
        return self.__height

    def __mul__(self, scale_factor):
        return Dimensions(self.width * scale_factor, self.height * scale_factor)

    def __truediv__(self, other):
        return Dimensions(self.width / other.width, self.height / other.height)

    def __str__(self):
        return f"{self.width}x{self.height}"


class BoundingBox:
    """Represents a bounding box around an object in an image."""

    def __init__(self, upper_left: Point, dimensions: Dimensions):
        self.__upper_left = upper_left
        self.__dimensions = dimensions

    @property
    def upper_left_corner(self) -> Point:
        """Get the bounding box's upper left corner."""
        return self.__upper_left

    @property
    def dimensions(self) -> Dimensions:
        """Get the bounding box's dimensions."""
        return self.__dimensions

    def __str__(self) -> str:
        # pylint: disable=line-too-long
        return f"{self.upper_left_corner.x},{self.upper_left_corner.y},{self.dimensions.width},{self.dimensions.height}"


class Frame:
    """Represents a single frame from a video sequence."""

    def __init__(self, frame_number: int, image: PIL.Image, ground_truth: BoundingBox):
        self.__frame_number = frame_number
        self.__image = image
        self.__ground_truth = ground_truth

    @property
    def number(self) -> int:
        """Get the this frame's number within the sequence. Numbering starts from 0."""
        return self.__frame_number

    @property
    def image(self) -> PIL.Image:
        """Get this frame's image."""
        return self.__image

    @property
    def ground_truth(self) -> BoundingBox:
        """Get the frame's ground truth bounding box."""
        return self.__ground_truth

    @property
    def width(self) -> int:
        """Get the width of the frame image, measured in pixels."""
        return self.image.size[0]

    @property
    def height(self) -> int:
        """Get the height of the frame image, measured in pixels."""
        return self.image.size[1]

    @property
    def dimensions(self) -> Dimensions:
        """Get the dimensions of the frame image, measured in pixels."""
        return Dimensions(self.width, self.height)

    def __str__(self) -> str:
        return f"{self.number}: {self.ground_truth}"

    def __mul__(self, scale_factor):
        """
        Resize the frame by the given scale factor.

        :param scale_factor: A scalar value used to scale the frame.
        :returns: A copy of this frame, scaled by the ``scale_factor``.
        :rtype: Frame
        :raises TypeError: if ``frame`` is not a Frame object, or if ``size`` is not a numeric type.
        """
        new_image_size = (
            int(self.image.size[0] * scale_factor),
            int(self.image.size[1] * scale_factor),
        )
        return Frame(
            self.number,
            self.image.resize(new_image_size),
            scale_and_move(self.ground_truth, scale_factor),
        )


def draw_bounding_box(frame: Frame, box: BoundingBox = None) -> Frame:
    """
    Draw a bounding box in a frame's image.

    :param Frame frame: The frame on which to draw the bounding box.
    :param BoundingBox box: The bounding box to draw. If this is ``None``, ``frame.ground_truth`` is
        used.
    :returns: A copy of ``frame``, with the bounding box drawn on it.
    :rtype: Frame
    """
    canvas = PIL.ImageDraw.Draw(frame.image)
    if box is None:
        box = frame.ground_truth
    canvas.rectangle(create_pillow_box(box), outline=(0, 255, 128), width=1)
    return frame


def draw_label(frame: Frame, label: str = None) -> Frame:
    """
    Draw a label in the upper left corner of the frame.

    :param Frame frame: The frame on which to draw the label.
    :param str label: The label to draw. If this is ``None``, ``frame.number`` is used.
    :returns: A copy of ``frame``, with the label drawn on it.
    :rtype: Frame
    """
    canvas = PIL.ImageDraw.Draw(frame.image)
    if label is None:
        label = f"#{frame.number:03}"
    yellow = (255, 204, 0)
    canvas.text(xy=(5, 5), text=label, fill=yellow)
    return frame


def scale_and_move(box, scale_factor):
    """
    Resize a bounding box, and move it based on the scale factor.

    :param BoundingBox box: The bounding box to resize and move.
    :param scale_factor: The scale factor for resizing and moving. This should be a scalar
        number; non-uniform scaling is not supported.
    :returns: The given ``box`` in its new location and with its new dimensions.
    :rtype: BoundingBox
    """
    return BoundingBox(
        box.upper_left_corner * scale_factor, box.dimensions * scale_factor
    )


def create_pillow_box(box):
    """
    Convert a bounding box to the list of pixel coordinates expected by
    PIL.ImageDraw.ImageDraw.rectangle().

    :param BoundingBox box: The bounding box to convert.
    :returns: The pixel coordinates for upper left and lower right corners of the bounding box.
    :rtype: list
    """
    return [
        box.upper_left_corner.x,
        box.upper_left_corner.y,
        box.upper_left_corner.x + box.dimensions.width,
        box.upper_left_corner.y + box.dimensions.height,
    ]


class _SelectionIterator:
    """Iterator for sequence.Selection objects."""

    def __init__(self, selection):
        self.__selection = selection
        self.__next_index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Frame:
        if self.__next_index < len(self.__selection.frames):
            frame = self.__selection.frames[self.__next_index]
            self.__next_index += 1
            return frame
        raise StopIteration


class Selection:
    """
    Defines a selection of frames from an image sequence.

    The frames do not need to be contiguous, nor in order. The only constraint is that the frame
    indices be >= 0, and less than the number of frames in the sequence.
    """

    def __init__(
        self,
        name: str,
        frames: list,
        root_path: str = os.path.expanduser("~/Videos/otb"),
    ):
        sequence_path = os.path.join(root_path, name)
        self.__name = name
        self.__frames = _load_selected_frames(sequence_path, frames)

    @property
    def name(self) -> str:
        """Get the name of the sequence."""
        return self.__name

    @property
    def frames(self) -> list:
        """Get the list of frames for the sequence selection."""
        return self.__frames

    def __iter__(self) -> _SelectionIterator:
        return _SelectionIterator(self)

    def __str__(self) -> str:
        string = f"Sequence: {self.name}\n"
        for frame in self.frames:
            string.append(f"  {frame}")
        return string

    def __len__(self) -> int:
        return len(self.frames)

    def __getitem__(self, index: int) -> Frame:
        return self.frames[index]

    def __contains__(self, frame_number: int) -> bool:
        for frame in self.frames:
            if frame.number == frame_number:
                return True
        return False

    def resize_to_width(self, new_width):
        scale = new_width / self[0].width
        self.__frames = [frame * scale for frame in self.__frames]


# --------------------------------------------------------------------------- implementation details
def _load_selected_frames(sequence_path: str, frame_numbers: list) -> list:
    imagery_path = os.path.join(sequence_path, "img")
    if not os.path.exists(imagery_path):
        raise FileNotFoundError(f"{imagery_path} does not exist")
    if not os.path.isdir(imagery_path):
        raise NotADirectoryError(f"{imagery_path} exists, but is not a directory")
    ground_truths = _load_ground_truth(sequence_path, frame_numbers)
    frames = []
    for i, frame_number in enumerate(frame_numbers):
        frame_path = os.path.join(imagery_path, f"{frame_number:04}.jpg")
        frames.append(Frame(frame_number, PIL.Image.open(frame_path), ground_truths[i]))
    return frames


def _load_ground_truth(sequence_path: str, frame_numbers: list) -> list:
    with open(os.path.join(sequence_path, "groundtruth_rect.txt")) as ground_truth_file:
        all_lines = ground_truth_file.readlines()
    lines = _filter_bounding_boxes(all_lines, frame_numbers)
    lines = [line.strip().split(",") for line in lines]
    return [
        BoundingBox(
            Point(int(line[0]), int(line[1])), Dimensions(int(line[2]), int(line[3]))
        )
        for line in lines
    ]


def _filter_bounding_boxes(all_boxes: list, frame_numbers: list) -> list:
    if len(frame_numbers) == len(all_boxes):
        return all_boxes
    boxes = []
    for frame_number in frame_numbers:
        boxes.append(all_boxes[frame_number - 1])
    return boxes
