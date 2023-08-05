# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import lxml
import csv


class Modifier(object):
    TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
    TEI = "{%s}" % TEI_NAMESPACE
    XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
    XML = "{%s}" % XML_NAMESPACE
    NSMAP = {None: TEI_NAMESPACE, "xml": XML_NAMESPACE}

    def __init__(self, target):
        self.namespaces = {"tei": "http://www.tei-c.org/ns/1.0",
                           "xml": "http://www.w3.org/XML/1998/namespace"}
        self._target = target

    @property
    def target(self):
        return self._target

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, filename):
        with open(filename) as file:
            reader = csv.DictReader(file, dialect="excel-tab")
            self._data = []
            for row in reader:
                self._data.append(row.copy())

    def modify(self):
        pass


class Place(Modifier):
    def modify(self):
        for row in self.data:
            expr = f"//*[@xml:id = \"{row['id']}\"]"
            place = self.target.tei_doc.xpath(expr)[0]
            placeName = place.xpath('tei:placeName',
                                    namespaces=self.namespaces)
            if len(placeName):
                placeName[0].text = row['placeName']
            else:
                placeName = ET.Element(self.TEI + "placeName",
                                       nsmap=self.NSMAP)
                placeName.text = row['placeName']
                place.append(placeName)

            if row['coordinate location']:
                location = lxml.etree.SubElement(place, self.TEI + "location",
                                                 nsmap=self.NSMAP)
                geo = lxml.etree.SubElement(location, self.TEI + "geo",
                                            nsmap=self.NSMAP)
                geo.text = row['coordinate location'].replace(',', ' ')

            if row['QID']:
                idno = lxml.etree.SubElement(place, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "WD")
                idno.text = row['QID']

            if ("dvp_id" in row.keys() and row['dvp_id']):
                idno = lxml.etree.SubElement(place, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "project")
                idno.text = row['dvp_id']


class Person(Modifier):
    def modify(self):
        for row in self.data:
            expr = f"//*[@xml:id = \"{row['id']}\"]"
            person = self.target.tei_doc.xpath(expr)[0]
            persName = person.xpath('tei:persName',
                                    namespaces=self.namespaces)
            if len(persName):
                persName[0].text = row['persName']
            else:
                persName = ET.Element(self.TEI + "persName",
                                      nsmap=self.NSMAP)
                persName.text = row['persName']
                person.append(persName)

            if row['QID']:
                idno = lxml.etree.SubElement(person, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "WD")
                idno.text = row['QID']

            if ("dvp_id" in row.keys() and row['dvp_id']):
                idno = lxml.etree.SubElement(person, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "project")
                idno.text = row['dvp_id']


class Org(Modifier):
    def modify(self):
        for row in self.data:
            expr = f"//*[@xml:id = \"{row['id']}\"]"
            org = self.target.tei_doc.xpath(expr)[0]
            orgName = org.xpath('tei:orgName',
                                   namespaces=self.namespaces)
            if len(orgName):
                orgName[0].text = row['orgName']
            else:
                orgName = ET.Element(self.TEI + "orgName",
                                       nsmap=self.NSMAP)
                orgName.text = row['orgName']
                org.append(orgName)

            if row['QID']:
                idno = lxml.etree.SubElement(org, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "WD")
                idno.text = row['QID']

            if ("dvp_id" in row.keys() and row['dvp_id']):
                idno = lxml.etree.SubElement(org, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "project")
                idno.text = row['dvp_id']


class Event(Modifier):
    def modify(self):
        for row in self.data:
            expr = f"//*[@xml:id = \"{row['id']}\"]"
            event = self.target.tei_doc.xpath(expr)[0]

            desc = event.xpath('tei:desc',
                               namespaces=self.namespaces)
            if len(desc):
                desc[0].text = row['name']
            else:
                desc = ET.Element(self.TEI + "desc",
                                     nsmap=self.NSMAP)
                desc.text = row['name']
                event.append(desc)

            if row['point in time']:
                event.set("when-iso", row['point in time'])

            if row['start time']:
                event.set("from-iso", row['start time'])

            if row['end time']:
                event.set("to-iso", row['end time'])

            if row['QID']:
                idno = lxml.etree.SubElement(event, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "WD")
                idno.text = row['QID']

            if ("dvp_id" in row.keys() and row['dvp_id']):
                idno = lxml.etree.SubElement(event, self.TEI + "idno",
                                             nsmap=self.NSMAP)
                idno.set("type", "project")
                idno.text = row['dvp_id']


class Standoff(Modifier):

    @property
    def iv_id(self):
        expr = f"//tei:fileDesc//tei:idno[@type='DDHI']"
        return self.target.tei_doc.xpath(expr,
                                         namespaces=self.namespaces)[0].text

    @property
    def stand_off(self):
        if self.target.standOff():
            return self.target.standOff()[0]
        else:
            return lxml.etree.SubElement(
                self.target.tei_doc.xpath("//tei:TEI",
                                          namespaces=self.namespaces)[0],
                self.TEI + "standOff",
                nsmap=self.NSMAP)

    @property
    def placeNames(self):
        return self.target.tei_doc.xpath("//tei:body//tei:placeName",
                                         namespaces=self.namespaces)

    @property
    def eventNames(self):
        return self.target.tei_doc.xpath("//tei:body//tei:name[@type='event']",
                                         namespaces=self.namespaces)

    @property
    def persNames(self):
        return self.target.tei_doc.xpath("//tei:body//tei:persName",
                                         namespaces=self.namespaces)

    @property
    def orgNames(self):
        return self.target.tei_doc.xpath("//tei:body//tei:orgName",
                                         namespaces=self.namespaces)

    def modify(self):
        self.mark_places()
        self.mark_events()
        self.mark_persons()
        self.mark_orgs()

    def mark_places(self):
        listPlace = lxml.etree.SubElement(self.stand_off,
                                          self.TEI + "listPlace",
                                          nsmap=self.NSMAP)
        for name in self.placeNames:
            place_id = f"{self.iv_id}_place_{self.placeNames.index(name)}"
            place = lxml.etree.SubElement(listPlace, self.TEI + "place",
                                          nsmap=self.NSMAP)
            place.set(self.XML + "id", place_id)
            pname = lxml.etree.SubElement(place, self.TEI + "placeName",
                                          nsmap=self.NSMAP)
            pname.text = name.text
            name.set("ref", f"#{place_id}")

    def mark_events(self):
        listEvent = lxml.etree.SubElement(self.stand_off,
                                          self.TEI + "listEvent",
                                          nsmap=self.NSMAP)

        for name in self.eventNames:
            event_id = f"{self.iv_id}_event_{self.eventNames.index(name)}"
            event = lxml.etree.SubElement(listEvent, self.TEI + "event",
                                          nsmap=self.NSMAP)
            event.set(self.XML + "id", event_id)
            desc = lxml.etree.SubElement(event, self.TEI + "desc",
                                         nsmap=self.NSMAP)
            desc.text = name.text
            name.set("ref", f"#{event_id}")

    def mark_persons(self):
        listPerson = lxml.etree.SubElement(self.stand_off,
                                           self.TEI + "listPerson",
                                           nsmap=self.NSMAP)
        for name in self.persNames:
            person_id = f"{self.iv_id}_person_{self.persNames.index(name)}"
            person = lxml.etree.SubElement(listPerson, self.TEI + "person",
                                           nsmap=self.NSMAP)
            person.set(self.XML + "id", person_id)
            pname = lxml.etree.SubElement(person, self.TEI + "persName",
                                          nsmap=self.NSMAP)
            pname.text = name.text
            name.set("ref", f"#{person_id}")

    def mark_orgs(self):
        listOrg = lxml.etree.SubElement(self.stand_off,
                                        self.TEI + "listOrg",
                                        nsmap=self.NSMAP)
        for name in self.orgNames:
            org_id = f"{self.iv_id}_org_{self.orgNames.index(name)}"
            org = lxml.etree.SubElement(listOrg, self.TEI + "org",
                                        nsmap=self.NSMAP)
            org.set(self.XML + "id", org_id)
            pname = lxml.etree.SubElement(org, self.TEI + "orgName",
                                          nsmap=self.NSMAP)
            pname.text = name.text
            name.set("ref", f"#{org_id}")
