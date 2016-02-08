""" Utilities to play with executable files.

Includes a standalone tool to demangle VC names on Windows directly from command
line input, using DbgHelp.UnDecorateSymbolName:

    $ python -m pyshgck.exe "?xyz@?$abc@V?$def@H@@PAX@@"
    abc<class def<int>,void *>::z

As you can see, it sorta works but doesn't seem to be able to handle all cases.
Maybe I should try with a different dbghelp.dll, but the one on my system is
already much more recent than the binaries where I've extracted those names.
"""

import argparse
import ctypes
import ctypes.util
import platform

MAX_DEMANGLED_LEN = 2**12


def demangle_vc(name, flags = 0x2800):
    """ Call DbgHelp.UnDecorateSymbolName and return the demangled name bytes.
    Default flags are UNDNAME_32_BIT_DECODE | UNDNAME_NO_ARGUMENTS because it
    seems to work only this way?! """
    if platform.system() != "Windows":
        print("DbgHelp is only available on Windows!")
        return b""

    dbghelp_path = ctypes.util.find_library("dbghelp")
    dbghelp = ctypes.windll.LoadLibrary(dbghelp_path)

    name = name.lstrip(".")
    mangled = ctypes.c_char_p(name.encode("utf8"))
    demangled = ctypes.create_string_buffer(b"\x00" * MAX_DEMANGLED_LEN)
    demangled_len = ctypes.c_int(MAX_DEMANGLED_LEN)
    flags = ctypes.c_int(flags)
    ret = dbghelp.UnDecorateSymbolName(mangled, demangled, demangled_len, flags)
    if ret == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        print("UnDecorateSymbolName failed ({})".format(error_code))
        return b""
    else:
        return demangled.value


DESCRIPTION = "Python interface to DbgHelp.UnDecorateSymbolName"

def main():
    argparser = argparse.ArgumentParser(description = DESCRIPTION)
    argparser.add_argument("name", type = str, help = "mangled name")
    args = argparser.parse_args()

    demangled = demangle_vc(args.name)
    if demangled:
        print(demangled.decode("utf8", errors = "replace"))


if __name__ == "__main__":
    main()
