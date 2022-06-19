#! /usr/bin/env python

import logging
import sys
from os import path

from password import Password


def main() -> int:
    generate = Password(2, 20)
    generate.run()
    logging.info("Bey!")
    return 0


if __name__ == "__main__":
    EXIT_STATUS = 1
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Script %s has started", path.basename(__file__))
    try:
        EXIT_STATUS = main()
    except Exception as e:
        logging.exception(e)
        EXIT_STATUS = 2
    finally:
        sys.exit(EXIT_STATUS)
