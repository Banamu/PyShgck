""" Utilities for parsing binary data. """


def read_cstring(file_object):
    """ Read the 0-terminated string from file_object at position offset and
    return corresponding bytes object (terminator excluded). """
    cstring = b""
    while True:
        char = file_object.read(1)
        if char and char != b"\x00":
            cstring += char
        else:
            break
    return cstring

# def read_utf16_string(file_object, offset, utf16_mode = False):
#     string_bytes = b""
#     current_offset = offset
#     while True:
#         file_object.seek(current_offset)
#         next_byte = file_object.read(1)
#         if not next_byte:
#             break
#         if next_byte == b"\x00":
#             if not (utf16_mode and (current_offset - offset) % 2 != 0):
#                 break
#         string_bytes += next_byte
#         current_offset += 1
#     return string_bytes

# def read_utf16be_string():
#     pass



def read_struct(file_object, struct):
    """ Read a struct.Struct from file_object and return the unpacked tuple. """
    data = file_object.read(struct.size)
    return struct.unpack(data)

def pad_data(data, padding, start_at = 0):
    """ Pad a piece of data according to the padding value and returns the
    result. Use start_at to specify an offset at the starting point. """
    while (start_at + len(data)) % padding != 0:
        data += b"\x00"
    return data
