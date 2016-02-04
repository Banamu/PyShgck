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
                  , "uu_codec", "zlib_codec" ) )


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
    """ Return decoded data, or None if decoding failed or the codec isn't
    usable on this machine. """
    try:
        return codecs.decode(data, encoding, "strict")
    except (UnicodeDecodeError, LookupError):
        return None

_WRITE_LOG_FAIL    = "{:<15} {}\n"
_WRITE_LOG_SUCCESS = "{:<15} -> {}\n"

def _write_log(results, logger):
    for encoding in results:
        result = results[encoding]
        if result is None:
            logger.write(_WRITE_LOG_FAIL.format(encoding, "decoding failed"))
        else:
            _try_write_log(encoding, result, logger)

def _try_write_log(encoding, result, logger):
    try:
        logger.write(_WRITE_LOG_SUCCESS.format(encoding, result))
    except UnicodeEncodeError:
        logger.write(_WRITE_LOG_FAIL.format(
            encoding, "decoding succeeded, but stdout doesn't support it"
        ))


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
