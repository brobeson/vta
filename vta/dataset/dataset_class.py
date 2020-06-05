"""Classes to encapsulate datasets and sequences."""

import os.path


class Frame:
    """Encapsulates information about a single frame within a sequence."""

    def __init__(self):
        pass

    @property
    def index(self):
        """The index of this frame within the sequence. This is 1-based, not 0-based."""

    @property
    def attributes(self):
        """
        The list of challenge attributes for this frame. This returns an empty list for datasets
        such as OTB, which do not provide per-frame attributes.
        """

    @property
    def ground_truth(self):
        """
        The ground truth bounding box for this frame. This is always a list of numbers, but the
        length of the list and the interpretation of the values varies from dataset to dataset.
        """

    @property
    def image(self):
        """
        The image for this frame. The image loaded and returned as-is; in particular, the image is
        not implicitly converted to RGB.
        """


class Sequence:
    """Metadata and operations on a visual tracking sequence."""

    def __init__(self):
        pass

    @property
    def name(self):
        """The name of the sequence."""

    @property
    def path(self):
        """The root file system path of the sequence."""

    @property
    def attributes(self):
        """
        The list of challenge attributes for this sequence. This returns an empty list for datasets
        such as VOT, which provide per-frame attributes.
        """

    def __len__(self):
        """The number of frames in the sequence."""

    def __getitem__(self, index):
        """Get a specific frame from the sequence."""

    def __iter__(self):
        """Get an iterator into the sequence."""

    def __reversed__(self):
        """Get a reverse iterator into the sequence."""


class Dataset:
    """Metadata and operations on a visual tracking dataset."""

    def __init__(self, name: str, path: str):
        if not isinstance(name, str):
            raise TypeError("A dataset name must be a string.")
        if not isinstance(path, str):
            raise TypeError("A dataset path must be a string.")
        if not os.path.isdir(path):
            raise ValueError(f"{path} does not exist as a dataset")
        self.__name = name
        self.__path = path
        self.__sequences = load_sequences(self.__path)

    @property
    def name(self) -> str:
        """The name of the dataset."""
        return self.__name

    @property
    def path(self):
        """The root file system path for the dataset."""
        return self.__path

    def __len__(self):
        """Get the number of sequences in the dataset."""

    def __getitem__(self, sequence_name):
        """Get the sequence known by ``sequence_name``."""

    def __iter__(self):
        """Get an iterator into the dataset."""

    def __reversed__(self):
        """Get a reverse iterator into the dataset."""

    def __contains__(self, sequence_name):
        """Query if a sequence is in the dataset."""


def load_sequences(path: str) -> list:
    """
    Load a list of sequences from a dataset.

    :param str path: The root path of the dataset.
    :returns: A list of ``Sequence`` objects.
    :rtype: list
    """
    sequence_names = [entry for entry in os.listdir(path) if os.path.isdir(entry)]
    return sequence_names
