import re
import secrets
import string
from shutil import get_terminal_size
from typing import ClassVar

from .passwordgeneratorexception import PasswordGeneratorException


class SingletonMeta(type):
    _instance: ClassVar = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    # def __del__(cls) -> None:
    # @IMPORTANT: is this working?
    # cls._instance = None
    # del cls._instance


class PasswordGenerator(metaclass=SingletonMeta):
    def __init__(self, min_patter: int = 1, length: int = 15, punctuation: str = "") -> None:
        self.all_strings = string.ascii_lowercase
        self.all_strings += string.ascii_uppercase
        self.all_strings += string.digits

        if punctuation:
            self.all_strings += punctuation
        else:
            self.all_strings += string.punctuation
        self.possible_pattern_type = 4
        self.columns = get_terminal_size().columns
        self.check_input(min_patter, length)
        self.length = length
        self.min_patter = min_patter

    def check_input(self, min_patter: int, length: int) -> None:
        """
        make sure all parameters passed are valid and usable
        """
        if not isinstance(min_patter, int) or min_patter < 1:
            raise PasswordGeneratorException("minimum patter must be an integer and positive")
        if not isinstance(length, int) or length < (min_patter * self.possible_pattern_type):
            msg = "length must be an integer and greater than "
            msg += str(min_patter * self.possible_pattern_type)
            raise PasswordGeneratorException(msg)
        if length > self.columns:
            raise PasswordGeneratorException("Password won't fix screen")

    def display(self) -> None:
        """
        display password to user in a easy & pretty way to ready
        """
        # https://pbs.twimg.com/media/FQGyvmxXwAIEMfp.png
        patt = "*"
        empty = " "
        side_column = 4
        phrase = self.get()
        both_side_columns = side_column * 2
        empty_length = self.columns - both_side_columns

        if int((empty_length - len(phrase)) / 2) > 0:
            margin = int((empty_length - len(phrase)) / 2)
            main_part = f"{patt:*>{side_column}}{empty: >{margin}}"
            main_part += phrase
            main_part += f"{empty: <{margin}}{patt:*<{side_column}}"
        elif int((self.columns - len(phrase)) / 2) > 0:
            margin = int((self.columns - len(phrase)) / 2)
            main_part = f"{empty: >{margin}}"
            main_part += phrase
            main_part += f"{empty: <{margin}}"
        else:
            main_part = phrase
        print(f"{patt:*^{self.columns}}")
        print(f"{patt:*^{self.columns}}")
        print(f"{patt:*^{self.columns}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(main_part)
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}")
        print(f"{patt:*^{self.columns}}")
        print(f"{patt:*^{self.columns}}")
        print(f"{patt:*^{self.columns}}")

    def generate(self) -> str:
        """
        generate a random password from self.all_strings characters
        """
        password = ""
        for _ in range(self.length):
            password += secrets.choice(seq=self.all_strings)
        return password

    def has_min_lowercase(self, password: str) -> bool:
        """
        validate password has minimun amount of lower case characters
        """
        count = sum(int(c.islower()) for c in password)
        return count >= self.min_patter

    def has_min_uppercase(self, password: str) -> bool:
        """
        validate password has minimun amount of upper case characters
        """
        count = sum(int(c.isupper()) for c in password)
        return count >= self.min_patter

    def has_min_digits(self, password: str) -> bool:
        """
        validate password has minimun amount of digits
        """
        count = sum(int(c.isdigit()) for c in password)
        return count >= self.min_patter

    def has_min_esp_char(self, password: str) -> bool:
        """
        validate password has minimun amount of espcial characters
        """
        regex = re.compile(r"[a-zA-Z0-9]")
        min_esp_char = regex.sub("", password)
        count = sum(int(c.isprintable()) for c in min_esp_char)
        return count >= self.min_patter

    def validate_password(self, password: str) -> bool:
        """
        validate password contains min_patter
        """
        condition1 = self.has_min_digits(password) and self.has_min_esp_char(password)
        condition2 = self.has_min_lowercase(password) and self.has_min_uppercase(password)
        return condition1 and condition2

    def get(self) -> str:
        """
        get a valid password
        """
        password = ""
        while not self.validate_password(password):
            password = self.generate()
        return password

    @classmethod
    def destroy(cls) -> None:
        del cls
