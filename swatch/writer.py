# encoding: utf-8
"""
swatch, a parser for adobe swatch exchange files
Copyright (c) 2014 Marcos A Ojeda http://generic.cx/

With notes from
http://iamacamera.org/default.aspx?id=109 and
http://www.colourlovers.com/ase.phps

All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""
import logging
import struct
import os


def chunk_count(swatch):
    if type(swatch) is dict:
        if 'data' in swatch:
            return 1
        if 'swatches' in swatch:
            return len(swatch['swatches'])
    else:
        return sum(map(chunk_count, swatch))

def chunk_for_dict(obj):
    # will prepend the total length of the chunk as a 4 byte int

    title = (obj['name']+'\0')
    title_length = len(title)
    chunk = struct.pack('>H', title_length)
    chunk += title.encode('utf-16be')

    mode = obj['data']['mode']
    values = obj['data']['values']
    color_type = obj['type']

    fmt = {b'RGB': '!fff', b'Gray': '!f', b'CMYK': '!ffff', b'LAB': '!fff'}
    if mode in fmt:
        chunk += struct.pack('!4s', str(mode).ljust(4)) # color name
        chunk += struct.pack(fmt[mode], *values) # the color values

    color_types = ['Global', 'Spot', 'Process']
    if color_type in color_types:
        color_int = color_types.index(color_type)
        chunk += struct.pack('>h', color_int) # append swatch mode

    chunk = struct.pack('>I', len(chunk)) + chunk # prepend the chunk size
    return b'\x00\x01' + chunk # swatch color header
