#! /usr/bin/env python

import logging
import sys
from os import path
import cProfile
import pstats
from password import PasswordGenerator


def main() -> int:
    with cProfile.Profile() as profile_output:
        generate = PasswordGenerator(2, 20)
        generate.display()
    stats = pstats.Stats(profile_output)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats("passwordgenerator", 30)
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
