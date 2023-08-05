# -*- coding: utf-8 -*-
# Transform code borrowed borrowed
# https://www.programcreek.com/python/example/96248/lxml.etree.XSLT
from lxml import etree
import logging


logger = logging.getLogger(__name__)


def xml_object(path_to_file):
    try:
        xml_obj = etree.parse(path_to_file)
    except etree.XMLSyntaxError as e:
        logger.error(e)
        raise
    return xml_obj


class Transformer:
    def transform_with_xsl(self, xsl_path, xml_path):
        stylesheet = etree.XSLT(xml_object(xsl_path))
        xml_obj = xml_object(xml_path)
        transformed_dom = stylesheet(xml_obj)
        return transformed_dom
