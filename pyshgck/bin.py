""" Utilities for parsing binary data. """


def read_cstring(file_object):
    """ Read the 0-terminated string from file_object and return the bytes
    object (terminator excluded). """
    cstring = b""
    while True:
        char = file_object.read(1)
        if char and char != b"\x00":
            cstring += char
        else:
            break
    return cstring

def read_utf16_string(file_object):
    """ Read a 0-terminated UTF16 string from file_object and return the bytes
    object (terminator excluded). This assumes that strings are stored with a
    uint16 null terminator, and should work with UTF16 LE as well as BE. """
    utf16_string = b""
    while True:
        wide_char = file_object.read(2)
        if wide_char and wide_char != b"\x00\x00":
            utf16_string += wide_char
        else:
            break
    return utf16_string

def read_struct(file_object, struct):
    """ Read a struct.Struct from file_object and return the unpacked tuple. """
    data = file_object.read(struct.size)
    return struct.unpack(data)


def pad_file(file_object, pad_amount, pad_value = b"\x00", start_at = 0):
    """ Pad a file opened in write mode according to the padding value.
    Use start_at to specify an offset at the starting point. """
    end_position = file_object.tell() + start_at
    if end_position % pad_amount != 0:
        pad_size = pad_amount - (end_position % pad_amount)
        file_object.write(pad_value * pad_size)

def pad_data(data, pad_amount, pad_value = b"\x00", start_at = 0):
    """ Pad a piece of data according to the padding value and returns the
    result. Use start_at to specify an offset at the starting point. """
    end_position = len(data) + start_at
    if end_position % pad_amount != 0:
        pad_size = pad_amount - (end_position % pad_amount)
        data += pad_value * pad_size
    return data
