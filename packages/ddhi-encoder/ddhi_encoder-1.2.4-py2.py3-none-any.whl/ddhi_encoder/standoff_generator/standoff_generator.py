# -*- coding: utf-8 -*-
from lxml import etree


class StandoffGenerator(object):
    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    XML_NAMESPACE = "http://www.w3.org/xml/1998/namespace"
    XML = "{%s}" % XML_NAMESPACE

    NSMAP = {None: TEI_NAMESPACE}  # default namespace

    def __init__(self, doc):
        self._tei_doc = doc
        self.namespaces = {"tei": "http://www.tei-c.org/ns/1.0",
                           "xml": "http://www.w3.org/XML/1998/namespace"}


    @property
    def tei_doc(self):
        return self._tei_doc

