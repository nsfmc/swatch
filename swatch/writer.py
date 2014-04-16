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
    """return the number of byte-chunks in a swatch object

    this recursively walks the swatch list, returning 1 for a single color &
    returns 2 for each folder plus 1 for each color it contains
    """
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
    """builds up a byte-chunk for a color

    the format for this is
        b'\x00\x01' +
        Big-Endian Unsigned Int == len(bytes that follow in this block)
          • Big-Endian Unsigned Short == len(color_name)
              in practice, because utf-16 takes up 2 bytes per letter
              this will be 2 * (len(name) + 1)
              so a color named 'foo' would be 8 bytes long
          • UTF-16BE Encoded color_name terminated with '\0'
              using 'foo', this yields '\x00f\x00o\x00o\x00\x00'
          • A 4-byte char for Color mode ('RGB ', 'Gray', 'CMYK', 'LAB ')
              note the trailing spaces
          • a variable-length number of 4-byte length floats
              this depends entirely on the color mode of the color.
          • A Big-Endian short int for either a global, spot, or process color
              global == 0, spot == 1, process == 2

    the chunk has no terminating string although other sites have indicated
    that the global/spot/process short is a terminator, it's actually used
    to indicate how illustrator should deal with the color.
    """
    title = obj['name'] + '\0'
    title_length = len(title)
    chunk = struct.pack('>H', title_length)
    chunk += title.encode('utf-16be')

    mode = obj['data']['mode'].encode()
    values = obj['data']['values']
    color_type = obj['type']

    fmt = {b'RGB': '!fff', b'Gray': '!f', b'CMYK': '!ffff', b'LAB': '!fff'}
    if mode in fmt:
        padded_mode = mode.decode().ljust(4).encode()
        chunk += struct.pack('!4s', padded_mode) # the color mode
        chunk += struct.pack(fmt[mode], *values) # the color values

    color_types = ['Global', 'Spot', 'Process']
    if color_type in color_types:
        color_int = color_types.index(color_type)
        chunk += struct.pack('>h', color_int) # append swatch mode

    chunk = struct.pack('>I', len(chunk)) + chunk # prepend the chunk size
    return b'\x00\x01' + chunk # swatch color header

def chunk_for_folder(obj):
    """produce a byte-chunk for a folder of colors

    the structure is very similar to a color's data:
    • Header
        b'\xC0\x01' +
        Big Endian Unsigned Int == len(Bytes in the Header Block)
          note _only_ the header, this doesn't include the length of color data
          • Big Endian Unsigned Short == len(Folder Name + '\0')
              Note that Folder Name is assumed to be utf-16be so this
              will always be an even number
          • Folder Name + '\0', encoded UTF-16BE
    • body
        chunks for each color, see chunk_for_color
    • folder terminator
        b'\xC0\x02' +
        b'\x00\x00\x00\x00'

    Perhaps the four null bytes represent something, but i'm pretty sure
    they're just a terminating string, but there's something nice about
    how the b'\xC0\x02' matches with the folder's header
    """
    title = obj['name'] + '\0'
    title_length = len(title)
    chunk_body = struct.pack('>H', title_length) # title length
    chunk_body += title.encode('utf-16be') # title

    chunk_head = b'\xC0\x01' # folder header
    chunk_head += struct.pack('>I', len(chunk_body))
    # precede entire chunk by folder header and size of folder
    chunk = chunk_head + chunk_body

    chunk += b''.join([chunk_for_color(c) for c in obj['swatches']])

    chunk += b'\xC0\x02' # folder terminator chunk
    chunk += b'\x00\x00\x00\x00' # folder terminator
    return chunk
