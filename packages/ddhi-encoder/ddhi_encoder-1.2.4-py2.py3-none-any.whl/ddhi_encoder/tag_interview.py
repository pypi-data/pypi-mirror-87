# -*- coding: utf-8 -*-
import sys
import os
import argparse
import logging
import spacy
from ddhi_encoder.interview import Interview


__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def tag_interview(inpath, outpath, nlp):
    interview = Interview(inpath, nlp)
    interview.tag()
    interview.write(outpath)


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Add named-entity tags to a TEI transcript")
    parser.add_argument("path_to_input",
                        help="the file(s) to tag")
    parser.add_argument('-m', '--model',
                        help="Spacy model to use",
                        default="en_core_web_sm")
    parser.add_argument("-o", "--path_to_output",
                        help="where to write the file(s)",
                        default=sys.stdout.buffer)
    return parser.parse_args(args)


def main(args):
    """Main entry point allowing external calls
    """
    args = parse_args(args)
    nlp = spacy.load(args.model)

    if os.path.isfile(args.path_to_input):
        # tag_interview(args.path_to_input, sys.stdout.buffer, nlp)
        tag_interview(args.path_to_input, args.path_to_output, nlp)
    elif os.path.isdir(args.path_to_input) and os.path.isdir(args.path_to_output):
        for root, dirs, files in os.walk(args.path_to_input):
            for fname in files:
                if fname.endswith(".xml"):
                    in_path = os.path.join(root, fname)
                    out_path = os.path.join(args.path_to_output, fname)
                    tag_interview(in_path, out_path, nlp)

    else:
        raise IOError()


def run():
    """Entry point for console_scripts.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
