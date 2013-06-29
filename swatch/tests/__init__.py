# encoding: utf-8
"""
swatch.tests

Solarized color palette using LAB data from
http://ethanschoonover.com/solarized

Copyright (c) 2012 Marcos A Ojeda http://generic.cx/
All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""

import unittest
import os
import swatch
import json


class TestSwatchParser(unittest.TestCase):
    """Tests for parser.py"""

    def compare_with_json(self, basepath):
        base = os.path.join("tests", basepath)
        with open(base + ".json") as f:
            ase = swatch.parse(base + ".ase")
            js = json.load(f)
            return js, ase

    def test_LAB(self):
        js, ase = self.compare_with_json("solarized")
        self.assertEqual(js, ase, "LAB test fails with solarized data")

    def test_empty_file(self):
        js, ase = self.compare_with_json("empty white folder")
        self.assertEqual(js, ase, "empty named folder no longer parses")

    def test_RGB(self):
        js, ase = self.compare_with_json("sampler")
        self.assertEqual(js, ase, "RGB test fails with sampler")

if __name__ == '__main__':
    unittest.main()
