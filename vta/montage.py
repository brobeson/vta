"""Main module for the vta montage command."""

import PIL.Image

import vta.utilities.sequence as sequence


def main():
    """Entry point for the vta montage application."""
    seq = [
        sequence.draw_label(sequence.draw_bounding_box(frame * 0.5))
        for frame in sequence.Selection("DragonBaby", [1, 2, 3, 4, 5])
    ]
    create_montage(seq)


def create_montage(frames) -> PIL.Image:
    """
    Create a montage from the supplied sequence frames.

    :param frames: An iterable container of ``sequence.Frame`` objects.
    :returns: A montage image created from the supplied frames.
    :rtype: PIL.Image
    """
    white = (255, 255, 255)
    border = 5
    montage_size = _calculate_montage_size(frames, border)
    montage = PIL.Image.new(
        mode="RGB", size=(montage_size.width, montage_size.height), color=white
    )
    for i, frame in enumerate(frames):
        montage.paste(frame.image, (border + i * (frame.image.width + border), border))
    montage.show()


def _calculate_montage_size(frames, border) -> sequence.Dimensions:
    width = 0
    height = 0
    for frame in frames:
        width += frame.image.size[0]
        height = max(height, frame.image.size[1])
    return sequence.Dimensions(width + (len(frames) + 1) * border, height + 2 * border)


if __name__ == "__main__":
    main()
