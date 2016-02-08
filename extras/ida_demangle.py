""" IDAPython plugin to demangle the string under the cursor and set the result
as comment.

As IDAPython is for Python 2 only and PyShgck is a Python 3 project, it is not
possible to use the system-wide Python 3 installed packages, where PyShgck
should reside. That's why the exe module is copied here.
"""

import ctypes
import ctypes.util
import platform

import idc

MAX_DEMANGLED_LEN = 2**12


def demangle_vc(name, flags = 0x2800):
    """ Call DbgHelp.UnDecorateSymbolName and return the demangled name bytes.
    Default flags are UNDNAME_32_BIT_DECODE | UNDNAME_NO_ARGUMENTS because it
    seems to work only this way?! """
    if platform.system() != "Windows":
        print "DbgHelp is only available on Windows!"
        return ""

    dbghelp_path = ctypes.util.find_library("dbghelp")
    dbghelp = ctypes.windll.LoadLibrary(dbghelp_path)

    name = name.lstrip(".")
    mangled = ctypes.c_char_p(name.encode("utf8"))
    demangled = ctypes.create_string_buffer("\x00" * MAX_DEMANGLED_LEN)
    demangled_len = ctypes.c_int(MAX_DEMANGLED_LEN)
    flags = ctypes.c_int(flags)
    ret = dbghelp.UnDecorateSymbolName(mangled, demangled, demangled_len, flags)
    if ret == 0:
        error_code = ctypes.windll.kernel32.GetLastError()
        print "UnDecorateSymbolName failed ({})".format(error_code)
        return ""
    else:
        return demangled.value


def main():
    ea = idc.ScreenEA()
    string = idc.GetString(ea)
    if not string:
        print("Couldn't get any string at {}.".format(hex(ea)))
        return

    demangled = demangle_vc(string)
    if not demangled:
        print("Demangling failed.")
        return

    idc.MakeComm(ea, demangled)


if __name__ == "__main__":
    main()
