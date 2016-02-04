import os
from os.path import dirname, join, isfile
import unittest

from pyshgck.logger import get_logger


FILES_DIR = join(dirname(__file__), "files")
LOG_FILE_PATH = join(FILES_DIR, "dummy.log")


class LoggerTests(unittest.TestCase):

    def setUp(self):
        LoggerTests._remove_log_file()

    @staticmethod
    def _remove_log_file():
        if isfile(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

    def test_logger(self):
        logger = get_logger(into_stderr = True, into_log_file = LOG_FILE_PATH)

        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")
        logger.critical("critical")

        log_file_size = os.stat(LOG_FILE_PATH).st_size
        self.assertNotEqual(log_file_size, 0)


if __name__ == '__main__':
    unittest.main()
