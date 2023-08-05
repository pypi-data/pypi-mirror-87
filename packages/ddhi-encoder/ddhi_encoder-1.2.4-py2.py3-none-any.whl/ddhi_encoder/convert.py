# -*- coding: utf-8 -*-
"""
This is a console script for invoking the
docx converter from the command line.

This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = ddhi_encoder.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging
from ddhi_encoder.interview_generator import InterviewGeneratorFactory
from ddhi_encoder import __version__

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def convert_doc(doc_path, out_path):
    factory = InterviewGeneratorFactory()
    interview = factory.interview_for("DDHI", doc_path)
    interview.update_tei()
    interview.to_file(out_path)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Convert a DVP Word-formatted xscript to TEI")
    parser.add_argument(
        "--version",
        action="version",
        version="ddhi-encoder {ver}".format(ver=__version__))

    parser.add_argument('file', help="the Word docx file to process")

    parser.add_argument('-o', '--outfile',
                        dest="outfile",
                        default=sys.stdout.buffer,
                        help="output file (stdout by default)")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.DEBUG)

    return parser.parse_args(args)


def setup_logging(loglevel):
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting conversion...")
    convert_doc(args.file, args.outfile)
    _logger.info("Conversion complete.")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
