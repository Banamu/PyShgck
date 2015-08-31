""" Utilities for parsing binary data. """


def read_cstring(data, offset, utf16_mode = False):
    """ Read the 0-terminated string from data at position offset and return
    corresponding bytes object (terminator excluded).

    If utf16_mode is true, it doesn't stop reading on the null bytes caused by
    smaller Unicode code points. In little-endian, that's just checking for an
    even offset to stop. It works, r-right?
    """
    string_bytes = b""
    current_offset = offset
    while True:
        data.seek(current_offset)
        next_byte = data.read(1)
        if not next_byte:
            break
        if next_byte == b"\x00":
            if not (utf16_mode and (current_offset - offset) % 2 != 0):
                break
        string_bytes += next_byte
        current_offset += 1
    return string_bytes

def read_struct(file_object, struct):
    """ Read a struct.Struct from file_object and return the unpacked tuple. """
    data = file_object.read(struct.size)
    return struct.unpack(data)


def pad_data(data, padding, start_at = 0):
    while (start_at + len(data)) % padding != 0:
        data += b"\x00"
    return data
