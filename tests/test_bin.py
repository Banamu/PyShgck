import os.path
import unittest

from shgck_tools.bin import read_cstring, read_struct, pad_data


FILES_DIR = os.path.join(os.path.dirname(__file__), "files")

CSTRING_FILE_PATH = os.path.join(FILES_DIR, "cstring_and_garbage.bin")
ASCII_DUMMY = "test string".encode("ascii")

UTF16_FILE_PATH = os.path.join(FILES_DIR, "utf16_and_garbage.bin")
UTF16_DUMMY = "ソウルシリーズ".encode("utf16")

FOUR_BYTES = b"aaaa"


class BinTests(unittest.TestCase):

    def setUp(self):
        self.ascii_file = open(CSTRING_FILE_PATH, "rb")
        self.utf16_file = open(UTF16_FILE_PATH, "rb")

    def tearDown(self):
        self.ascii_file.close()
        self.utf16_file.close()

    def test_read_cstring(self):
        cstring = read_cstring(self.ascii_file, 0)
        self.assertEquals(cstring, ASCII_DUMMY)
        
        cstring = read_cstring(self.utf16_file, 0, utf16_mode = True)
        self.assertEquals(cstring, UTF16_DUMMY)

    def test_pad_data(self):
        padded_to_16 = pad_data(FOUR_BYTES, 16)
        padded_to_16_expected = FOUR_BYTES + (12 * b"\x00")
        self.assertEquals(padded_to_16, padded_to_16_expected)

        padded_to_16_plus_8 = pad_data(FOUR_BYTES, 16, start_at = 8)
        padded_to_16_plus_8_expected = FOUR_BYTES + (4 * b"\x00")
        self.assertEquals(padded_to_16_plus_8, padded_to_16_plus_8_expected)


if __name__ == '__main__':
    unittest.main()
