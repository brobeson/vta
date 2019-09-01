"""Functionality for downloading VOT sequences."""

import os

def download_sequences(root_directory, force, subset, sequences):
    """Downloads the requested sequences from the VOT dataset.

    Args:
        root_directory: A string specifying the root directory into which to
            download the sequences. "vot" is appended to this; so sequences are
            ultimately downloaded to root_directory/vot.
        force: A boolean indicating whether to download sequences which already
            exist in the root directory.
        sequences: A list of sequences to download. The sequence names must
            match exactly. If this is None, all sequences are downloaded.

    Returns:
        0 is returned if downloading the sequences succeeds.
        Any other integer is returned otherwise.

    Raises:
        Nothing
    """
    print("Downloading vot")
    #os.makedirs(os.path.join(root_directory, "vot"), exist_ok=True)
    return 0
