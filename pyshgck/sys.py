""" Utilities for system programming and environment detection. """

import os
import platform
import sys


################################################################################
# Privileges
################################################################################

def is_running_as_root():
    """ Return True is this is running as root on a Linux machine. """
    return platform.system() == "Linux" and os.geteuid() == 0


################################################################################
# Architecture
################################################################################

def is_64bit_python():
    """ Return True if the Python interpreter is 64-bit. """
    return sys.maxsize > 2**32

def is_64bit_system():
    """ Return True if the OS is 64-bit. """
    return platform.machine().endswith("64")


################################################################################
# Environment
################################################################################

def is_running_in_ida():
    try:
        import idc
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    print("Arch:", "64-bit" if is_64bit_system() else "32-bit")
    print("Interpreter:", "64-bit" if is_64bit_python() else "32-bit")
