""" Utilities related to computer architecture. """

import platform
import sys


def is_64bit_python():
    """ Return True if the Python interpreter is 64-bit. """
    return sys.maxsize > 2**32

def is_64bit_system():
    """ Return True if the OS is 64-bit. """
    return platform.machine().endswith("64")


if __name__ == "__main__":
    print("Arch:", "64-bit" if is_64bit_system() else "32-bit")
    print("Interpreter:", "64-bit" if is_64bit_python() else "32-bit")
