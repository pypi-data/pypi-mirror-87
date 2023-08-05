# -*- coding: utf-8 -*-
from lxml import etree
import sys
import csv


class NeExtractor:
    """Extracts named entities from a TEI document."""

    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    XML_NAMESPACE = "http://www.w3.org/xml/1998/namespace"
    XML = "{%s}" % XML_NAMESPACE

    def __init__(self, path_to_tei):
        self.tei_doc = etree.parse(
            path_to_tei, etree.XMLParser(remove_blank_text=True))
        self.namespaces = {"tei": "http://www.tei-c.org/ns/1.0",
                           "xml": "http://www.w3.org/XML/1998/namespace"}

    def places(self):
        return self.tei_doc.xpath("//tei:standOff//tei:place",
                                  namespaces=self.namespaces)

    def persons(self):
        return self.tei_doc.xpath("//tei:standOff//tei:person",
                                  namespaces=self.namespaces)

    def orgs(self):
        return self.tei_doc.xpath("//tei:standOff//tei:org",
                                  namespaces=self.namespaces)

    def events(self):
        return self.tei_doc.xpath("//tei:standOff//tei:event",
                                  namespaces=self.namespaces)

    def place_names_list(self):
        places = self.places()
        thelist = list()
        for place in places:
            id = place.get('{http://www.w3.org/XML/1998/namespace}id')
            placeName = place.xpath(".//tei:placeName",
                                    namespaces=self.namespaces)[0].text
            thelist.append({'id': id, 'placeName': placeName})
        return thelist

    def person_names_list(self):
        persons = self.persons()
        thelist = list()
        for person in persons:
            id = person.get('{http://www.w3.org/XML/1998/namespace}id')
            persName = person.xpath(".//tei:persName",
                                    namespaces=self.namespaces)[0].text
            thelist.append({'id': id, 'persName': persName})
        return thelist

    def org_names_list(self):
        orgs = self.orgs()
        thelist = list()
        for org in orgs:
            id = org.get('{http://www.w3.org/XML/1998/namespace}id')
            orgName = org.xpath(".//tei:orgName",
                                    namespaces=self.namespaces)[0].text
            thelist.append({'id': id, 'orgName': orgName})
        return thelist

    def event_names_list(self):
        events = self.events()
        thelist = list()
        for event in events:
            id = event.get('{http://www.w3.org/XML/1998/namespace}id')
            desc = event.xpath(".//tei:desc",
                               namespaces=self.namespaces)[0].text
            thelist.append({'id': id, 'name': desc})
        return thelist

    def to_tsv(self, list, stream=sys.stdout):
        writer = csv.DictWriter(stream,
                                fieldnames=[k for k in list[0].keys()],
                                delimiter="\t")
        writer.writeheader()
        for row in list:
            writer.writerow(row)
