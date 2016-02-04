""" A standalone tool to try all Python encodings on a text file. """

import argparse
import codecs
import encodings.aliases
import sys


DESCRIPTION = "Try various encodings for this text file."
LOGFILE_ARG_HELP = "log file, use - to output on stdout"

# Get all the encodings names directly from the standard aliases dict, but
# remove special irrelevant encodings that will raise specific exceptions.
ENCODINGS = set(encodings.aliases.aliases.values())
ENCODINGS -= set( ( "base64_codec", "bz2_codec", "hex_codec", "rot_13"
                  , "tactis", "uu_codec", "zlib_codec" ) )


def try_encodings(data, log_file):
    """ Try to decode data for all known encodings (see codecs module doc),
    store output in a file named log_file, or stdout if log_file is '-'. """
    results = {}
    for encoding in ENCODINGS:
        results[encoding] = try_encoding(encoding, data)

    if log_file != "-":
        with open(log_file, "w", encoding = "utf8") as log:
            _write_log(results, log)
    else:
        _write_log(results, sys.stdout)

def try_encoding(encoding, data):
    """ Return decoded data, or None if decoding failed. """
    try:
        print(data)
        return codecs.decode(data, encoding, "strict")
    except UnicodeDecodeError:
        return None


def _write_log(results, logger):
    for encoding in results:
        result = results[encoding] or "<decoding failed>"
        logger.write("{:<15} -> {}\n".format(encoding, result))


def main():
    argparser = argparse.ArgumentParser(description = DESCRIPTION)
    argparser.add_argument("input_file", type = str, help = "file to test")
    argparser.add_argument("log_file", type = str, help = LOGFILE_ARG_HELP)
    args = argparser.parse_args()

    with open(args.input_file, "rb") as input_file:
        data = input_file.read()

    try_encodings(data, args.log_file)


if __name__ == "__main__":
    main()
