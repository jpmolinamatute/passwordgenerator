import secrets
import string
from os import get_terminal_size
from typing import ClassVar

from .passwordexception import PasswordException


class SingletonMeta(type):
    _instances: ClassVar[dict] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Password(metaclass=SingletonMeta):
    def __init__(
        self, min_patter: int = 1, length: int = 10, accepted_punctuation: str = ""
    ) -> None:
        self.all_strings = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
        ]
        if accepted_punctuation:
            self.all_strings.append(accepted_punctuation)
        else:
            self.all_strings.append(string.punctuation)
        self.columns = get_terminal_size().columns
        self.check_input(min_patter, length)
        self.length = length
        self.min_patter = min_patter

    def check_input(self, min_patter: int, length: int) -> None:
        if not isinstance(min_patter, int) or min_patter < 1:
            raise PasswordException("minimum patter must be an integer and positive")
        if not isinstance(length, int) or length < (min_patter * len(self.all_strings)):
            msg = "length must be an integer and greater than "
            msg += str(min_patter * len(self.all_strings))
            raise PasswordException(msg)
        if length > self.columns:
            raise PasswordException("Password won't fix screen")

    def get_min_mandatory(self) -> list[str]:
        mandatory: list[str] = []
        for _ in range(self.min_patter):
            mandatory += self.all_strings

        return mandatory

    def get_mandatory(self) -> str:
        mandatory = self.get_min_mandatory()
        result = ""
        while mandatory:
            index = secrets.choice(range(0, len(mandatory)))
            result += secrets.choice(mandatory[index])
            mandatory.pop(index)
        return result

    @staticmethod
    def display(phrase: str, max_length: int = 150) -> None:
        # https://pbs.twimg.com/media/FQGyvmxXwAIEMfp.png
        patt = "*"
        empty = " "
        side_column = 4
        both_side_columns = side_column * 2
        empty_length = max_length - both_side_columns

        if int((empty_length - len(phrase)) / 2) > 0:
            margin = int((empty_length - len(phrase)) / 2)
            main_part = f"{patt:*>{side_column}}{empty: >{margin}}"
            main_part += phrase
            main_part += f"{empty: <{margin}}{patt:*<{side_column}}"
        elif int((max_length - len(phrase)) / 2) > 0:
            margin = int((max_length - len(phrase)) / 2)
            main_part = f"{empty: >{margin}}"
            main_part += phrase
            main_part += f"{empty: <{margin}}"
        else:
            main_part = phrase
        print(f"{patt:*^{max_length}}")
        print(f"{patt:*^{max_length}}")
        print(f"{patt:*^{max_length}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(main_part)
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*^{max_length}}")
        print(f"{patt:*^{max_length}}")
        print(f"{patt:*^{max_length}}")

    def run(self) -> None:
        whole_sample = "".join(self.all_strings)
        mandatory = self.get_mandatory()
        length_left = self.length - len(mandatory)
        for _ in range(length_left):
            mandatory += secrets.choice(seq=whole_sample)

        self.display(mandatory, self.columns)
