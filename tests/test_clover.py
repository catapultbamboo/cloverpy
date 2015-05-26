import os
import xml.etree.ElementTree as ET
import unittest

from cloverpy import clover


class TestCase(unittest.TestCase):

    def test_convert(self):
        coverage = os.path.join(os.path.dirname(__file__), 'coverage.xml')
        clover_xml = clover.convert(coverage)
        root = ET.fromstring(clover_xml)
        timestamp = root.find('./project').attrib.get('timestamp')
        self.assertEquals(timestamp, '1429279546472')
        metrics = root.find('./project/metrics')
        attrib = dict(
            packages="1", files="13", classes="13",
            complexity="0", loc="682", ncloc="682",
            elements="682", statements="682",
            coveredelements="592", coveredstatements="592",
            coveredconditionals="0", conditionals="0",
            methods="0", coveredmethods="0")
        self.assertEquals(metrics.attrib, attrib)


if __name__ == '__main__':
    unittest.main()
