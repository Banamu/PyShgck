# encoding: utf8

from os.path import dirname, join
import unittest

from pyshgck.encodings import try_encodings


FILES_DIR = join(dirname(__file__), "files")

DUMMY_TEXT_FILE_PATH = join(FILES_DIR, "dummy.txt")


class BinTests(unittest.TestCase):

    def test_try_encodings(self):
        with open(DUMMY_TEXT_FILE_PATH, "rb") as dummy_text_file:
            binary_text = dummy_text_file.read()
            try_encodings(binary_text, '-')


if __name__ == '__main__':
    unittest.main()
