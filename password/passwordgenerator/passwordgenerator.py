import inspect
import random
import re
import secrets
import string
import timeit
from shutil import get_terminal_size
from typing import ClassVar

from .passwordgeneratorexception import PasswordGeneratorException


class SingletonMeta(type):
    _instance: ClassVar = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

    def __del__(cls) -> None:
        del cls._instance


class PasswordGenerator(metaclass=SingletonMeta):
    """
    Generate a random password with the following rules:
    - At least `min_pattern` lowercase letter
    - At least `min_pattern` uppercase letter
    - At least `min_pattern` digit
    - At least `min_pattern` special character
    - Length of `length`
    """

    def __init__(self, min_pattern: int = 1, length: int = 15, punctuation: str = "") -> None:
        self.possible_pattern_type = 4
        self.columns = get_terminal_size().columns
        self.check_input(min_pattern, length)
        self.punctuation = punctuation
        self.length = length
        self.min_pattern = min_pattern

    def all_characters(self) -> str:
        """
        Return all possible characters to use in password
        """
        raw_all_ascii = f"{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}"
        if self.punctuation:
            raw_all_ascii += self.punctuation
        else:
            raw_all_ascii += string.punctuation

        result = "".join(random.sample(raw_all_ascii, self.length))
        return "".join(random.sample(result, self.length))

    @property
    def password(self) -> str:
        """
        get a valid password
        """

        password = ""
        while not self.validate_password(password):
            password = self.generate()

        return password

    def check_input(self, min_pattern: int, length: int) -> None:
        """
        make sure all parameters passed are valid and usable
        """
        if not isinstance(min_pattern, int) or min_pattern < 1:
            raise PasswordGeneratorException("minimum patter must be an integer and positive")
        if not isinstance(length, int) or length < (min_pattern * self.possible_pattern_type):
            msg = "length must be an integer and greater than "
            msg += str(min_pattern * self.possible_pattern_type)
            raise PasswordGeneratorException(msg)
        if length > self.columns:
            raise PasswordGeneratorException("Password won't fix screen")

    def display(self) -> None:
        """
        display password to user in a easy & pretty way to ready
        reference: https://pbs.twimg.com/media/FQGyvmxXwAIEMfp.png
        """

        patt = "*"
        empty = " "
        side_column = 4
        phrase = self.password
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

        output = f"""
            {patt:*^{self.columns}}
            {patt:*^{self.columns}}
            {patt:*^{self.columns}}
            {patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}
            {patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}
            {main_part}
            {patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}
            {patt:*>{side_column}}{empty: >{empty_length}}{patt:*<{side_column}}
            {patt:*^{self.columns}}
            {patt:*^{self.columns}}
            {patt:*^{self.columns}}
        """
        print(inspect.cleandoc(output))

    def generate(self) -> str:
        """
        generate a random password from self.all_characters
        """

        all_characters = self.all_characters()
        password = ""
        for _ in range(self.length):
            password += secrets.choice(seq=all_characters)
        return password

    def has_min_lowercase(self, password: str) -> bool:
        """
        validate password has minimun amount of lower case characters
        """

        count = sum(int(c.islower()) for c in password)
        return count >= self.min_pattern

    def has_min_uppercase(self, password: str) -> bool:
        """
        validate password has minimun amount of upper case characters
        """

        count = sum(int(c.isupper()) for c in password)
        return count >= self.min_pattern

    def has_min_digits(self, password: str) -> bool:
        """
        validate password has minimun amount of digits
        """

        count = sum(int(c.isdigit()) for c in password)
        return count >= self.min_pattern

    def has_min_esp_char(self, password: str) -> bool:
        """
        validate password has minimun amount of espcial characters
        """

        regex = re.compile(r"[a-zA-Z0-9]")
        min_esp_char = regex.sub("", password)
        count = sum(int(c.isprintable()) for c in min_esp_char)
        return count >= self.min_pattern

    def validate_password(self, password: str) -> bool:
        """
        validate password contains min_pattern
        """

        condition1 = self.has_min_digits(password) and self.has_min_esp_char(password)
        condition2 = self.has_min_lowercase(password) and self.has_min_uppercase(password)
        return condition1 and condition2
