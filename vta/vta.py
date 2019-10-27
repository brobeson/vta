"""The main entry point for all VTA commands."""

import argparse
import os.path
import sys

import yaml

from vta.dataset import dataset
from vta.graph import graph
from vta.loss import loss


def main():
    """Runs VTA commands, as if vta were run via a command line.

    This function is the main entry point for all VTA commands. Running this
    function in your script is equivalent to running VTA from the command line.

    :return: An exit code following Unix command conventions. 0 indicates
        that command processing succeeded. Any other value indicates that an
        error occurred.
    :rtype: int
    """
    master_parser = make_parser()
    arguments = master_parser.parse_args()
    if arguments.configuration:
        configuration = load_configuration(arguments.configuration)
    else:
        configuration = None
    if arguments.command == "dataset":
        return dataset.main(arguments)
    if arguments.command == "graph":
        return graph.main(arguments, configuration)
    if arguments.command == "loss":
        return loss.main(arguments, configuration)
    return 0


def make_parser():
    """Create the argument parser for the root VTA command.

    :return: The argument parser, with all common arguments and subparsers
        added.
    :rtype: :py:class:`argparse.ArgumentParser`
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
    common_options = argparse.ArgumentParser(add_help=False)
    common_options.add_argument(
        "--configuration",
        help="Specify a VTA configuration file to read. The configuration file"
        " format is YAML.",
        default=os.path.expanduser("~/.vta.yml"),
        metavar="PATH",
    )
    # dataset.make_parser(subparsers)
    graph.make_parser(subparsers, common_options)
    loss.make_parser(subparsers, common_options)
    return master_parser


def load_configuration(file_path):
    """Load a VTA configuration file.

    :param str file_path: The path to the configuration file.
    :return: The configuration read from file_path.
    :rtype: dict
    :raises OSError: if opening file_path fails.
    """
    file_path = os.path.expanduser(file_path)
    try:
        with open(file_path) as config_file:
            configuration = yaml.load(config_file, yaml.FullLoader)
    except OSError:
        sys.exit(f"I could not open {file_path}.")
    if configuration is None:
        sys.exit(f"{file_path} does not appear to contain VTA configuration data.")
    return configuration


if __name__ == "__main__":
    sys.exit(main())
