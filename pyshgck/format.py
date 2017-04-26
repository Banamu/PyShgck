""" Utilities for formatting data. Can be run as a standalone tool. """

import argparse
import binascii
import json
import string


DESCRIPTION = "Hexdump and formatting utils"


def main():
    argparser = argparse.ArgumentParser(description=DESCRIPTION)
    argparser.add_argument("input_file", type=str, help="file to hexdump")
    args = argparser.parse_args()

    input_filepath = args.input_file
    try:
        with open(input_filepath, "rb") as input_file:
            data = input_file.read()
    except OSError as exc:
        print("Couldn't load {}: {}".format(input_filepath, exc))
        return

    print(get_data_dump(data))


################################################################################
# Small formatting functions
################################################################################

def hexlify(data):
    """ Short handle to get data as a readable str. """
    return binascii.hexlify(data).decode("ascii")

def get_json_dump(json_object, indent=4, sort_keys=False):
    """ Short handle to get a pretty printed str from a JSON object. """
    return json.dumps(json_object, indent=indent, sort_keys=sort_keys)


################################################################################
# Hexdump pretty printer
################################################################################

def get_data_dump(data):
    """ Return a pretty binary data representation in a Hexdump fashion. """
    dump = ""
    index = 0
    while index < len(data):
        data_slice = data[ index : index+16 ]
        offset_str = _get_offset_string(index)
        data_str = _get_hexdump_string(data_slice)
        ascii_str = _get_asciidump_string(data_slice)
        dump += "{} {:<47} {}\n".format(offset_str, data_str, ascii_str)
        index += 16
    return dump

def _get_offset_string(index):
    offset = hex(index)[2:]
    offset = offset.zfill(8)
    return offset

def _get_hexdump_string(data):
    hexdump = binascii.hexlify(data).decode("ascii")
    spaced_hexdump = ""
    index = 0
    while index < len(hexdump):
        spaced_hexdump += hexdump[ index : index+2 ] + " "
        index += 2
    return spaced_hexdump.strip()

def _get_asciidump_string(data):
    asciidump = ""
    for char in data:
        char = chr(char)
        if char in string.printable and not char in "\r\n\t":
            asciidump += char
        else:
            asciidump += "."
    return asciidump


if __name__ == "__main__":
    main()
