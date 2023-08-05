# -*- coding: utf-8 -*-
# word_parser.py

import re
from abc import ABC, abstractmethod
from docx2python import docx2python
from ddhi_encoder.utterance import Utterance


class WordParser(ABC):
    @abstractmethod
    def parse(self):
        pass


class DDHIParser(WordParser):
    def __init__(self):
        self.utt = re.compile(r"^([A-Za-z-]+):\s+(.*?)$")
        self.utterances = []

    def utterance(self, para):
        m = self.utt.match(para)
        if m:
            return Utterance(m.group(1), m.group(2).strip())

    def parse_old(self, path_to_docx):
        self._extracted = docx2python(path_to_docx)
        self.utterances = list(
            filter(None, [self.utterance(p)
                          for p in self._extracted.body[0][0][0]])
        )

    def parse(self, path_to_docx):
        self._extracted = docx2python(path_to_docx)
        in_body = False
        for p in self._extracted.body[0][0][0]:
            m = self.utt.match(p)
            if m:
                in_body = True
                self.utterances.append(Utterance(m.group(1), m.group(2)))
            elif in_body and len(p) > 0:
                self.utterances[-1].append(p.strip())


class WordParserFactory:
    def parser_for(self, project):
        if project == "DDHI":
            return DDHIParser()
