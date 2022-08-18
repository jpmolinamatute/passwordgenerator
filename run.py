#! /usr/bin/env python

import logging
import sys
from os import path
import argparse

from password import PasswordGenerator


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a secure password")
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=20,
        help="length of the password to be generated. Default 20",
    )
    parser.add_argument(
        "-m",
        "--min",
        type=int,
        dest="min_patter",
        default=2,
        help="minimim number of character per charactr type. Default 2",
    )
    parser.add_argument(
        "-p",
        "--punctuation",
        type=str,
        dest="accepted_punctuation",
        default="",
        help="valid puntuation. Default !\"#$&'()*+,-./:;<=>?@[\\]^_`{|}~%%",
    )
    raw_args = parser.parse_args()
    generate = PasswordGenerator(
        raw_args.min_patter,
        raw_args.length,
        raw_args.accepted_punctuation,
    )
    generate.display()
    return 0


if __name__ == "__main__":
    EXIT_STATUS = 1
    logging.basicConfig(level=logging.DEBUG)

    logging.info("Script %s has started", path.basename(__file__))
    try:
        EXIT_STATUS = main()
        logging.info("Bye!")
    except Exception as e:
        logging.exception(e)
        EXIT_STATUS = 2
    finally:
        sys.exit(EXIT_STATUS)
