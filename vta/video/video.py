"""The entry module for the vta boxes command."""

import argparse
import glob
import os.path

import cv2


def main(arguments, configuration):
    """Runs the vta video command.

    This is the main entry point for the VTA video command. It will draw bounding boxes on sequence
    frames.

    :param argparse.Namespace arguments: The command line arguments, as parsed by the
        :py:mod:`argparse` module. Run `vta boxes --help` for details.
    :return: An exit code following Unix command conventions. 0 indicates that command processing
        succeeded. Any other value indicates that an error occurred.
    :rtype: int
    """
    images, image_path = _load_sequence(
        configuration["datasets"].values(), arguments.sequence
    )

    # cv2.rectangle(image, (10 * i, 10 * i), (100, 100), (0, 0, 255, 255))
    height, width, _ = images[0].shape
    out = cv2.VideoWriter(
        arguments.output,
        cv2.VideoWriter_fourcc(*"DIVX"),
        arguments.fps,
        (width, height),
    )
    for i, image in enumerate(images):
        print(f"Writing image {i:04}")
        out.write(image)
    out.release()


def make_parser(subparsers, common_options):
    """Creates an argument parser for the VTA video command.

    :param subparsers: The sub-parsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The video argument parser will be added
        to this.
    :return: Nothing
    """
    parser = subparsers.add_parser(
        "video",
        help="Create a video from a tracking sequence.",
        prog="vta video",
        description="This command can be used to draw multiple bounding boxes on specific frames "
        "from a sequence.",
        parents=[common_options],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="The path to an output file for the video. If omitted, the image "
        "is displayed on screen.",
    )
    parser.add_argument(
        "--fps",
        type=int,
        help="The number of frames per second for the video.",
        default=30,
    )
    parser.add_argument("sequence", type=str, help="The name of the sequence.")


# -------------------------------------------------------------------------- implementation details
def _load_sequence(datasets: list, sequence: str) -> tuple:
    """Search the provided datasets for a specific sequence.

    :param list datasets: The paths to the datasets to search.
    :param str sequence: The name of the sequence to find.
    :return: The requested sequence images and the path to the images on disk. The path is useful to
        load metadata related to the image such as ground truth bounding boxes.
    :rtype: ([cv2 images], str)
    :raises FileNotFoundError: if the requested sequence  cannot be found in any of the
        supplied datasets.
    """
    otb_path = os.path.join(sequence, "img")  # , f"{frame:04}.jpg")
    vot_path = os.path.join(sequence, "color")  # , f"{frame:08}.jpg")
    for dataset in datasets:
        otb_path = os.path.join(dataset, sequence, "img")
        if os.path.exists(otb_path):
            return (_load_images(otb_path), otb_path)
        vot_path = os.path.join(dataset, sequence, "color")
        if os.path.exists(vot_path):
            return (_load_images(vot_path), vot_path)
    raise FileNotFoundError(
        f"Cannot find sequence '{sequence}' in the supplied datasets."
    )


def _load_images(sequence_path: str) -> list:
    images = []
    filenames = glob.glob(f"{sequence_path}/*.jpg")
    filenames.sort()
    for filename in filenames:
        images.append(cv2.imread(filename))
    return images
