"""Functionality for downloading VOT sequences."""

# def download_sequences(subsets, root_directory, force, sequences):
def download_sequences():
    """Downloads the requested sequences from the VOT dataset.

    :param list subsets: An optional list of subsets of VOT to download. If this
        is ``None``, all subsets will be downloaded.
    :param str root_directory: The root directory into which to download the
        sequences. *vot* is appended to this; so sequences are ultimately
        downloaded to *root_directory/vot*.
    :param bool force: If ``True``, sequences will be downloaded even if they
        already exists in ``root_directory``. If ``False``, existing sequences
        will not be downloaded again.
    :param list sequences: Specific sequences to download. The sequence names
        must match exactly. If this is ``None``, all sequences are downloaded.

    :return: Nothing
    """
    print("Downloading vot")
    # os.makedirs(os.path.join(root_directory, "vot"), exist_ok=True)
    return 0
