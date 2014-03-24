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
            return 2 + len(swatch['swatches'])
    else:
        return sum(map(chunk_count, swatch))

def chunk_for_object(obj):
    type = obj.get('type')
    if type == 'Color Group':
        return chunk_for_folder(obj)
    if type in ['Process', 'Spot', 'Global']:
        return chunk_for_color(obj)

def chunk_for_color(obj):
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

def chunk_for_folder(obj):
    title = obj['name'] + '\0'
    title_length = len(title)
    chunk_body = struct.pack('>H', title_length) # title length
    chunk_body += title.encode('utf-16be') # title

    chunk_head = b'\xC0\x01' # folder header
    chunk_head += struct.pack('>I', len(chunk_body))
    # precede entire chunk by folder header and size of folder
    chunk = chunk_head + chunk_body

    chunk += "".join([chunk_for_color(c) for c in obj['swatches']])

    chunk += b'\xC0\x02' # folder terminator chunk
    chunk += b'\x00\x00\x00\x00' # folder terminator
    return chunk
