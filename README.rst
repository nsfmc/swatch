Swatch
======

swatch is a parser for adobe swatch exchange files

Copyright (c) 2012 Marcos A Ojeda http://generic.cx/


With help from ASE documentation written by
`Carl Camera <http://iamacamera.org/default.aspx?id=109>`_ and
the ase generator written for colourlovers by
`Chris Williams <http://www.colourlovers.com/ase.phps>`_

``swatch.parse`` reads in an ase file and converts it to a list of colors and
palettes. colors are simple dicts of the form::

    {
        'name': u'color name',
        'type': u'Process',
        'data': {
            'mode': u'RGB',
            'values': [1.0, 1.0, 1.0]
        }
    }

the values provided vary between color mode. For all color modes, the
value is always a list of floats.

RGB: three floats between [0,1]  corresponding to RGB.
CMYK: four floats between [0,1] inclusive, corresponding to CMYK.
Gray: one float between [0,1] with 1 being white, 0 being black.
LAB: three floats. The first L, is ranged from 0,1. Both A and B are
floats ranging from [-128.0,127.0]. I believe illustrator just crops
these to whole values, though.

Palettes (Color Groups in Adobe Parlance) are also dicts, but they have an
attribute named ``swatches`` which contains a list of colors contained within
the palette.::

    {
        'name': u'accent colors',
        'type': u'Color Group',
        'swatches': [
            {color}, {color}, ..., {color}
        ]
    }

Because Adobe Illustrator lets swatches exist either inside and outside
of palettes, the output of swatch.parse is a list that may contain
swatches and palettes, i.e. [ swatch* palette* ]

Here's an example with a light grey swatch followed by a color group containing
three swatches::

    >>> import swatch
    >>> swatch.parse("example.ase")
    [{'data': {'mode': u'Gray', 'values': [0.75]},
      'name': u'Light Grey',
      'type': u'Process'},
     {'name': u'Accent Colors',
      'swatches': [{'data': {'mode': u'CMYK',
         'values': [0.5279774069786072,
          0.24386966228485107,
          1.0,
          0.04303044080734253]},
        'name': u'Green',
        'type': u'Process'},
       {'data': {'mode': u'CMYK',
         'values': [0.6261844635009766,
          0.5890134572982788,
          3.051804378628731e-05,
          3.051804378628731e-05]},
        'name': u'Violet Process Global',
        'type': u'Global'},
       {'data': {'mode': u'LAB', 'values': [0.6000000238418579, -35.0, -5.0]},
        'name': u'Cyan Spot (global)',
        'type': u'Spot'}],
      'type': u'Color Group'}]

Caveats
-------

Finally, consider the fact that your swatches can be CMYK a mixed blessing.
While this is invariably useful if you need to import some old swatches for
print work, it will pose a challenge for accurately converting back to RGB/LAB
unless you have a copy of illustrator handy.

If you don't, you can always install color profile calculator in the (oddly
named) `little cms <http://www.littlecms.com/>`_ and feed it the freely
available SWOP icc color profile and use the default output of sRGB to get
your colors in a somewhat usable form for the web.

If you end up with LAB spot colors, you can always pay
`Bruce Lindbloom <http://www.brucelindbloom.com/index.html?Math.html>`_ a
visit to get the relatively easy, if somewhat time consuming, LAB->XYZ->RGB
formulas.
