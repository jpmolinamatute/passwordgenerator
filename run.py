#! /usr/bin/env python

import logging
import secrets
import string
import sys
from os import path


def get_min_mandatory(min_sample: int) -> list[str]:
    all_strings = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]
    mandatory: list[str] = []
    for _ in range(min_sample):
        mandatory += all_strings

    return mandatory


def get_mandatory(min_sample: int = 1) -> str:
    if min_sample < 1:
        raise Exception("min value is 1")
    mandatory = get_min_mandatory(min_sample)

    result = ""
    while mandatory:
        index = secrets.choice(range(0, len(mandatory)))
        result += secrets.choice(mandatory[index])
        mandatory.pop(index)
    return result


def display(phrase: str) -> None:
    patt = "*"
    empty = " "
    max_length = 150
    margin = (max_length - len(phrase) - 6) / 2
    empty_length = max_length - 6
    print(f"{patt:*^{max_length}}")
    print(f"{patt:*^{max_length}}")
    print(f"{patt:*^{max_length}}")
    print(f"{patt:*^3}{empty: ^{empty_length}}{patt:*^3}")
    print(f"{patt:*^3}{empty: ^{empty_length}}{patt:*^3}")
    print(f"{patt:*^3}{empty: ^{margin}}{phrase}{empty: ^{margin}}{patt:*^3}")
    print(f"{patt:*^3}{empty: ^{empty_length}}{patt:*^3}")
    print(f"{patt:*^3}{empty: ^{empty_length}}{patt:*^3}")
    print(f"{patt:*^{max_length}}")
    print(f"{patt:*^{max_length}}")
    print(f"{patt:*^{max_length}}")


def main() -> int:
    size = 30
    min_patter = 3
    whole_sample = string.ascii_lowercase
    whole_sample += string.ascii_uppercase
    whole_sample += string.digits
    whole_sample += string.punctuation
    mandatory = get_mandatory(min_patter)
    size_left = size - len(mandatory)
    for _ in range(size_left):
        mandatory += secrets.choice(seq=whole_sample)
    display(mandatory)

    return 0


if __name__ == "__main__":
    EXIT_STATUS = 1
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Script %s has started", path.basename(__file__))
    try:
        EXIT_STATUS = main()
    except KeyboardInterrupt:
        logging.info("Bye!")
    except Exception as e:
        logging.exception(e)
        EXIT_STATUS = 2
    finally:
        sys.exit(EXIT_STATUS)
