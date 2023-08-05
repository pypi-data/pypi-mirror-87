# -*- coding: utf-8 -*-

import argparse
import sys
import csv
from ddhi_encoder.ne_extractor import NeExtractor
from ddhi_encoder import __version__

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


def to_tsv(list, stream=sys.stdout):
    writer = csv.DictWriter(stream,
                            fieldnames=[k for k in list[0].keys()],
                            delimiter="\t")
    writer.writeheader()
    for row in list:
        writer.writerow(row)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="export standoff places to tsv")
    parser.add_argument(
        "--version",
        action="version",
        version="ddhi-encoder {ver}".format(ver=__version__))

    parser.add_argument('file', help="the TEI document")

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
    extractor = NeExtractor(args.file)
    place_names_list = extractor.place_names_list()
    to_tsv(place_names_list)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
