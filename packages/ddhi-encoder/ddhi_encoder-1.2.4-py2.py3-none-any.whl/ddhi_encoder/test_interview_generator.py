# -*- coding: utf-8 -*-

import pytest
import re
import os
from ddhi_encoder.interview import InterviewGenerator, InterviewGeneratorFactory
from ddhi_encoder.word_parser import WordParserFactory
from ddhi_encoder.utterance import Utterance
import spacy

__author__ = "Clifford Wulfman"
__copyright__ = "Clifford Wulfman"
__license__ = "mit"


def test_interview():
    factory = WordParserFactory()
    testdoc = os.path.join(os.path.dirname(__file__), 'short.docx')
    template = os.path.join(os.path.dirname(__file__), 'teitemplate.xml')
    parser = factory.parser_for("DDHI")
    nlp = spacy.load("en_core_web_sm")

    interview = InterviewGenerator(parser, testdoc, template, nlp)
    assert interview.utterances[1].speaker == ('TAVELA')
    assert re.search('Washington', interview.utterances[1].speech)
    assert re.search('sourceDesc', interview.xml())


def test_interview_factory():
    factory = InterviewGeneratorFactory()
    testdoc = os.path.join(os.path.dirname(__file__), 'short.docx')
    interview = factory.interview_for("DDHI", testdoc)
    assert interview.utterances[1].speaker == ('TAVELA')
    assert re.search('Washington', interview.utterances[1].speech)
    assert re.search('sourceDesc', interview.xml())
    interview.update_tei()
    interview.to_file("/tmp/fluff.xml")
