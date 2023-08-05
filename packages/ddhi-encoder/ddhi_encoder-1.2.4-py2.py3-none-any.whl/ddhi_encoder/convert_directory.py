# -*- coding: utf-8 -*-
"""
This is a console script for converting a directory
of word docs to TEI xml.
"""

import argparse
import sys
import os
import logging
from ddhi_encoder.interview_generator import InterviewGeneratorFactory
from ddhi_encoder import __version__

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def convert_docs(in_path, out_path):
    for root, dirs, files in os.walk(in_path):
        for fname in files:
            if fname.endswith(".docx"):
                in_path = os.path.join(root, fname)
                out_path = os.path.join(root,
                                        fname.replace(".docx", ".tei.xml"))
                convert_doc(in_path, out_path)


def convert_doc(in_path, out_path):
    _logger.info("converting doc")
    factory = InterviewGeneratorFactory()
    interview = factory.interview_for("DDHI", in_path)
    interview.update_tei()
    _logger.info(" ".join(["writing to", out_path]))
    interview.to_file(out_path)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Convert a DVP Word-formatted xscript to TEI")
    parser.add_argument(
        "--version",
        action="version",
        version="ddhi-encoder {ver}".format(ver=__version__))

    parser.add_argument(
        dest="in_dir",
        help="the directory of Word docx files to process")

    parser.add_argument(
        dest="out_dir",
        help="where to write the converted files")

    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)

    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)

    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
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
    _logger.info("Starting conversion...")
    if not os.path.isdir(args.out_dir):
        raise FileNotFoundError(f"output directory |{args.out_dir}| not found")
    convert_docs(args.in_dir, args.out_dir)
    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
