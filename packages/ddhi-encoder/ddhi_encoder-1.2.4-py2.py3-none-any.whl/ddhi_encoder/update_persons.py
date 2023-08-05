# -*- coding: utf-8 -*-

import argparse
import sys
from ddhi_encoder.modifiers.modifiers import Person
from ddhi_encoder.interview import Interview
from ddhi_encoder import __version__

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="updates persons in standoff")
    parser.add_argument(
        "--version",
        action="version",
        version="ddhi-encoder {ver}".format(ver=__version__))

    parser.add_argument('tei', help="the TEI document")
    parser.add_argument('tsv', help="the tsv update document")

    parser.add_argument('-o', '--outfile',
                        dest="outfile",
                        default=sys.stdout.buffer,
                        help="output file (stdout by default)")

    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    interview = Interview()
    interview.read(args.tei)
    modifier = Person(interview)
    modifier.data = args.tsv
    modifier.modify()
    interview.write(args.outfile)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
