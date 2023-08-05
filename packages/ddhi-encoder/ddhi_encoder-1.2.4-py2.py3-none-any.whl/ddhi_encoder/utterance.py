# -*- coding: utf-8 -*-
# utterance.py

from lxml import etree
import re


class Utterance:
    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    NSMAP = {None: TEI_NAMESPACE}  # default namespace

    def __init__(self, speaker, speech):
        self.speaker = speaker
        self.speech = speech

    def __len__(self):
        return len(self.speech)

    @property
    def nlp(self):
        return self._nlp

    @nlp.setter
    def nlp(self, spacy_nlp_object):
        self._nlp = spacy_nlp_object

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, spacy_doc):
        self._doc = spacy_doc

    def process(self):
        self._doc = self.nlp(self.speech)

    def xml(self):
        utt_elem = etree.Element(self.TEI + "u",
                                 who=self.speaker, nsmap=self.NSMAP)
        utt_elem.text = self.speech
        # return etree.tostring(utt_elem)
        return utt_elem

    def append(self, text):
#        self.speech = self.speech + "\n\n" + text
        self.speech = self.speech + text
        return self.speech
