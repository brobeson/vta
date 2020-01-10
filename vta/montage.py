"""Main module for the vta montage command."""

import PIL.Image

import vta.utilities.sequence as sequence


def main():
    """Entry point for the vta montage application."""
    seq = [
        sequence.draw_label(sequence.draw_bounding_box(frame * 0.5))
        for frame in sequence.Selection("DragonBaby", [1, 2, 3, 4, 5, 6])
    ]
    create_montage(seq, sequence.Dimensions(3, 2))


def create_montage(frames, dimensions: sequence.Dimensions) -> PIL.Image:
    """
    Create a montage from the supplied sequence frames.

    :param frames: An iterable container of ``sequence.Frame`` objects.
    :param sequence.Dimensions dimensions: The dimensions of the montage, measured in columns and
        rows of images. So ``Dimenions(3, 2)`` will create a montage with six images, in three
        columns and two rows.
    :returns: A montage image created from the supplied frames.
    :rtype: PIL.Image
    """
    white = (255, 255, 255)
    border = 5
    frame_dimensions = frames[0].dimensions
    montage_size = _calculate_montage_size(frame_dimensions, dimensions, border)
    montage = PIL.Image.new(
        mode="RGB", size=(montage_size.width, montage_size.height), color=white
    )
    for i, frame in enumerate(frames):
        location = _calculate_frame_location(i, frame_dimensions, dimensions, border)
        montage.paste(frame.image, (location.x, location.y))
    montage.show()


def _calculate_montage_size(frame_dimensions, montage_dimensions, border):
    return sequence.Dimensions(
        montage_dimensions.width * (frame_dimensions.width + border) + border,
        montage_dimensions.height * (frame_dimensions.height + border) + border,
    )


def _calculate_frame_location(i, frame_dimensions, montage_dimensions, border):
    row = i // montage_dimensions.width
    column = i % montage_dimensions.width
    return sequence.Point(
        column * (frame_dimensions.width + border) + border,
        row * (frame_dimensions.height + border) + border,
    )


if __name__ == "__main__":
    main()
