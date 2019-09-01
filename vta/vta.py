"""The main entry point for all VTA commands."""

import argparse
import sys
from vta.dataset import dataset


def main():
    """Runs VTA commands, as if vta were run via a command line.

    This function is the main entry point for all VTA commands. Running this
    function in your script is equivalent to running VTA from the command line.

    :return: An exit code following Unix command conventions. 0 indicates
        that command processing succeeded. Any other value indicates that an
        error occurred.
    :rtype: int
    """
    master_parser = argparse.ArgumentParser(
        prog="vta",
        description="VTA is a suite of tools for analysing experimental results"
        " in the computer vision field of visual tracking. VTA provides several"
        " tools for various tasks common in conducting such research.",
    )
    master_parser.add_argument(
        "--version",
        action="version",
        help="Print the version of VTA, then exit.",
        version="1.0",
    )
    subparsers = master_parser.add_subparsers(
        title="VTA commands",
        description="These are the commands available in VTA.",
        dest="command",
    )
    dataset.make_parser(subparsers)
    arguments = master_parser.parse_args()
    if arguments.command == "dataset":
        return dataset.main(arguments)
    return 0


if __name__ == "__main__":
    sys.exit(main())
