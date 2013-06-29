# encoding: utf-8
"""
swatch, a parser for adobe swatch exchange files
Copyright (c) 2012 Marcos A Ojeda http://generic.cx/

With notes from
http://iamacamera.org/default.aspx?id=109 and
http://www.colourlovers.com/ase.phps

All Rights Reserved
MIT Licensed, see LICENSE.TXT for details
"""
import logging
import struct
import os


def parse_chunk(fd):
    chunk_type = fd.read(2)
    while chunk_type:
        if chunk_type == b'\x00\x01':
            # a single color
            logging.debug("[swatch.parser] parse_chunk saw single color")
            o = dict_for_chunk(fd)
            yield o

        elif chunk_type == b'\xC0\x01':
            # folder/palate
            logging.debug("[swatch.parser] parse_chunk saw folder")
            o = dict_for_chunk(fd)
            o['swatches'] = [x for x in colors(fd)]
            yield o

        elif chunk_type == b'\xC0\x02':
            # this signals the end of a folder
            logging.debug("[swatch.parser] parse_chunk saw end of folder")
            assert fd.read(4) == b'\x00\x00\x00\x00'
            pass

        else:
            # the file is malformed?
            logging.debug("[swatch.parser] parse_chunk got malformed ase file")
            assert chunk_type in [
                b'\xC0\x01', b'\x00\x01', b'\xC0\x02', b'\x00\x02']
            pass

        chunk_type = fd.read(2)


def colors(fd):
    chunk_type = fd.read(2)
    while chunk_type in [b'\x00\x01', b'\x00\x02']:
        d = dict_for_chunk(fd)
        yield d
        chunk_type = fd.read(2)
    fd.seek(-2, os.SEEK_CUR)


def dict_for_chunk(fd):
    chunk_length = struct.unpack(">I", fd.read(4))[0]
    data = fd.read(chunk_length)

    title_length = (struct.unpack(">H", data[:2])[0]) * 2
    title = data[2:2 + title_length].decode("utf-16be").strip('\0')
    color_data = data[2 + title_length:]

    output = {
        'name': str(title),
        'type': 'Color Group'  # default to color group
    }

    if color_data:
        fmt = {b'RGB': '!fff', b'Gray': '!f', b'CMYK': '!ffff', b'LAB': '!fff'}
        color_mode = struct.unpack("!4s", color_data[:4])[0].strip()
        color_values = list(struct.unpack(fmt[color_mode], color_data[4:-2]))

        color_types = ['Global', 'Spot', 'Process']
        swatch_type_index = struct.unpack(">h", color_data[-2:])[0]
        swatch_type = color_types[swatch_type_index]

        output.update({
            'data': {
                'mode': color_mode.decode('utf-8'),
                'values': color_values
            },
            'type': str(swatch_type)
        })

    return output
