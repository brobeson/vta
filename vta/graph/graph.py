"""The entry module for the vta graph command."""

import argparse
import pdb

def main(arguments, configuration):
    """Runs the vta graph command.

    This is the main entry point for the VTA graph command. It will draw graphs of object tracking
    results.

    :param argparse.Namespace arguments: The command line arguments, as parsed
        by the :py:mod:`argparse` module. Run `vta loss --help` for details.
    :param dict configuration: An optional run time configuration. In normal
        use, this will have been read from a YAML file.
    :return: An exit code following Unix command conventions. 0 indicates that
        command processing succeeded. Any other value indicates that an error
        occurred.
    :rtype: int
    """
    pdb.set_trace()
    configuration = configuration["graph"]


def make_parser(subparsers, common_options):
    """Creates an argument parser for the VTA graph command.

    :param subparsers: The subparsers object returned by a call to
        :py:func:`argparse.ArgumentParser.add_subparsers`. The graph argument parser will be added
        to this.
    :param common_options: The common options object, that will server as the parent parser to all
        command sub-parsers. This should already contain the options that are common to all
        commands.
    :return: Nothing
    """
    parser = subparsers.add_parser(
        "graph",
        help="Graph tracking results.",
        prog="vta graph",
        description="This command can be used to draw graphs of object tracking results.",
        parents=[common_options],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--trackers",
        help="A list of trackers to graph. Only these trackers will be graphed. To graph all"
        " trackers, just omit this option.",
        nargs="+",
        metavar="TRACKER",
    )
    parser.add_argument(
        "graph_type",
        help="The type of graph to generate.",
        choices=["success", "precision"],
    )
