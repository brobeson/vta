"""The entry module for the vta boxes command."""

import argparse
import os.path

import PIL.Image
import PIL.ImageDraw


def main(arguments, configuration):
    """Runs the vta boxes command.

    This is the main entry point for the VTA boxes command. It will draw bounding boxes on sequence
    frames.

    :param argparse.Namespace arguments: The command line arguments, as parsed by the
        :py:mod:`argparse` module. Run `vta boxes --help` for details.
    :return: An exit code following Unix command conventions. 0 indicates that command processing
        succeeded. Any other value indicates that an error occurred.
    :rtype: int
    """
    image, image_path = _load_image(
        configuration["datasets"].values(), arguments.sequence, arguments.frame
    )
    if image.mode != "RGB":
        image = image.convert("RGB")
    ground_truth = _load_ground_truth(image_path, arguments.frame)
    _draw_bounding_box(image, ground_truth)
    if arguments.output:
        image.save(arguments.output)
    else:
        image.show()


def make_parser(subparsers, common_options):
    """Creates an argument parser for the VTA boxes command.

    :param subparsers: The sub-parsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The boxes argument parser will be added
        to this.
    :return: Nothing
    """
    parser = subparsers.add_parser(
        "boxes",
        help="Draw bounding boxes on sequence frames.",
        prog="vta boxes",
        description="This command can be used to draw multiple bounding boxes on specific frames "
        "from a sequence.",
        parents=[common_options],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The path to an output file for the frame with bounding boxes drawn on it. If "
        "omitted, the image is displayed on screen.",
    )
    parser.add_argument("sequence", type=str, help="The name of the sequence.")
    parser.add_argument(
        "frame",
        type=int,
        help="The number of the frame on which to draw bounding boxes. The number must match the "
        "file numbering sequence in the dataset, but without leading zeros.",
    )


# -------------------------------------------------------------------------- implementation details
def _load_image(datasets: list, sequence: str, frame: int) -> tuple:
    """Search the provided datasets for a specific sequence and frame.

    :param list datasets: The paths to the datasets to search.
    :param str sequence: The name of the sequence to find.
    :param int frame: The index of the frame to find.
    :return: The requested frame image and the path to the image on disk. The path is useful to load
        metadata related to the image such as a ground truth bounding box.
    :rtype: (PIL.Image.Image, str)
    :raises FileNotFoundError: if the requested sequence and frame cannot be found in any of the
        supplied datasets.
    """
    otb_path = os.path.join(sequence, "img", f"{frame:04}.jpg")
    vot_path = os.path.join(sequence, "color", f"{frame:08}.jpg")
    for dataset in datasets:
        if os.path.exists(os.path.join(dataset, otb_path)):
            return (
                PIL.Image.open(os.path.join(dataset, otb_path)),
                os.path.join(dataset, otb_path),
            )
        if os.path.exists(os.path.join(dataset, vot_path)):
            return (
                PIL.Image.open(os.path.join(dataset, vot_path)),
                os.path.join(dataset, vot_path),
            )
    raise FileNotFoundError(
        f"Cannot find sequence '{sequence}', frame '{frame}' in the supplied datasets."
    )


def _load_ground_truth(image_path: str, frame: int) -> list:
    """Read the ground truth bounding box for the specified frame.

    :param str image_path: The path to the loaded image on disk.
    :param int frame: The index for the loaded frame.
    :returns: The ground truth bounding box data for the specified frame.
    :rtype: list of int
    """
    if "img" in image_path:
        gt_path = os.path.join(
            os.path.dirname(os.path.dirname(image_path)), "groundtruth_rect.txt"
        )
    else:
        gt_path = os.path.join(
            os.path.dirname(os.path.dirname(image_path)), "groundtruth.txt"
        )
    with open(gt_path) as gt_file:
        lines = gt_file.readlines()
    box = lines[frame - 1].strip().split(",")
    box = [float(coordinate) for coordinate in box]
    return box


def _draw_bounding_box(image: PIL.Image.Image, box: list) -> PIL.Image.Image:
    """
    Draw a bounding box on an image. The image is modified in place.

    :param PIL.Image.Image image: The image on which to draw the bounding box.
    :param list box: The bounding box to draw.
    :raises ValueError: if ``box`` does not contain 4 or 8 elements.
    """
    if len(box) != 4 and len(box) != 8:
        raise ValueError(f"A bounding box with {len(box)} is not valid.")
    canvas = PIL.ImageDraw.Draw(image)
    line_color = (0, 255, 0)
    line_width = 2
    if len(box) == 4:
        # OTB bounding box is a list: [x, y, width, height]
        canvas.rectangle(
            [(box[0], box[1]), (box[0] + box[2], box[1] + box[3])],
            outline=line_color,
            width=line_width,
        )
    else:
        # Use Draw.line() because Draw.polygon does not allow setting a width for the polygon edges.
        # The second call to Draw.line() closes the bounding box.
        canvas.line(box, fill=line_color, width=line_width)
        canvas.line([box[0], box[1], box[6], box[7]], fill=line_color, width=line_width)
