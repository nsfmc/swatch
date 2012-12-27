# encoding: utf-8
"""
swatch, a parser for adobe swatch exchange files
Copyright (c) 2012 Marcos A Ojeda http://generic.cx/

With notes from
http://iamacamera.org/default.aspx?id=109 by Carl Camera and
http://www.colourlovers.com/ase.phps by Chris Williams

All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""


__title__ = 'swatch'
__version__ = '0.1.0'
__author__ = 'Marcos Ojeda'
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Marcos A Ojeda'


from . import parser
import struct


def parse(filename):
    """parses a .ase file and returns a list of colors and palettes

    swatch.parse reads in an ase file and converts it to a list of colors and
    palettes. colors are simple dicts of the form

        {
            'name': u'color name',
            'data': {
                'mode': 'RGB',
                'values': [1.0, 1.0, 1.0]
            }
        }

    the values provided vary between color mode. For all color modes, the
    value is always a list of floats.

    RGB: three floats between [0,1]  corresponding to RGB
    CMYK: four floats between [0,1] inclusive, corresponding to CMYK
    Gray: one float between [0,1] with 1 being white, 0 being black
    LAB: three floats. The first L, is ranged from 0,1. Both A and B are
    floats ranging from [-128.0,127.0]. I believe illustrator just crops
    these to whole values, though.

    Palettes are also dicts, but they have an attribute named swatches which
    contains a list of colors contained within the palette.

        {
            'name': u'accent colors',
            'swatches': [
                {color}, {color}, ..., {color}
            ]
        }

    Because Adobe Illustrator lets swatches exist either inside and outside
    of palettes, the output of swatch.parse is a list that may contain
    swatches and palettes, i.e. [ [swatch|palette]* ]

    Here's an example:

    >>> import swatch
    >>> swatch.parse("simple palette.ase")
    [{'data': {'mode': 'RGB', 'values': [1.0, 1.0, 1.0]}, 'name': u'Bright White'}]

    """
    with open(filename, "rb") as data:
        header, version_major, version_minor, chunk_count = struct.unpack("!4sHHI", data.read(12))

        assert header == "ASEF"
        assert (version_major, version_minor) == (1, 0)

        return [c for c in parser.parse_chunk(data)]
