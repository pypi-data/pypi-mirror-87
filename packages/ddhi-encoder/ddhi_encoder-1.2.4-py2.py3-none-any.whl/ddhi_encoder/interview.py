# -*- coding: utf-8 -*-
# interview.py
from lxml import etree
from ddhi_encoder.ne_tagger import DDHINETagger


class Interview:
    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
    XML = "{%s}" % XML_NAMESPACE
    NSMAP = {None: TEI_NAMESPACE, "xml": XML_NAMESPACE}

    def __init__(self, docpath=None, nlp=None):
        self.namespaces = {"tei": "http://www.tei-c.org/ns/1.0"}
        if docpath:
            self.read(docpath)
        if nlp:
            self.nlp = nlp

    def read(self, path):
        self.tei_doc = etree.parse(path,
                                   etree.XMLParser(remove_blank_text=True))

    def write(self, path):
        if self.tei_doc:
            self.tei_doc.write(path,
                               pretty_print=True,
                               encoding='UTF-8')

    def dump(self):
        print(
            etree.tostring(self.tei_doc,
                           pretty_print=True,
                           encoding='unicode')
            )

    def tag(self):
        utts = self.tei_doc.xpath("//tei:u", namespaces=self.namespaces)
        for utt in utts:
            tagger = DDHINETagger(self.nlp, utt)
            tagger.tag()

    def places(self):
        return self.tei_doc.xpath("//tei:standOff/tei:listPlace/tei:place",
                                  namespaces=self.namespaces)

    def persons(self):
        return self.tei_doc.xpath("//tei:standOff/tei:listPerson/tei:person",
                                  namespaces=self.namespaces)
    
    def orgs(self):
        return self.tei_doc.xpath("//tei:standOff/tei:listOrg/tei:org",
                                  namespaces=self.namespaces)
    
    def events(self):
        return self.tei_doc.xpath("//tei:standOff/tei:listEvent/tei:event",
                                  namespaces=self.namespaces)

    def placeNames(self):
        return self.tei_doc.xpath("//tei:body//tei:placeName",
                                  namespaces=self.namespaces)

    def persNames(self):
        return self.tei_doc.xpath("//tei:body//tei:persName",
                                  namespaces=self.namespaces)

    def orgNames(self):
        return self.tei_doc.xpath("//tei:body//tei:orgName",
                                  namespaces=self.namespaces)

    def eventNames(self):
        return self.tei_doc.xpath("//tei:body//tei:name[@type='event']",
                                  namespaces=self.namespaces)

    def standOff(self):
        return self.tei_doc.xpath("//tei:standOff",
                                  namespaces=self.namespaces)
        
