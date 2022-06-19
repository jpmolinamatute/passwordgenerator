import secrets
import string


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Password(metaclass=SingletonMeta):
    def __init__(self, min_patter: int = 1, length: int = 10) -> None:
        self.all_strings = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation,
        ]
        if not self.check_input(min_patter, length):
            # @TODO: improve error message with something more descriptive
            raise Exception("invalid input")
        self.length = length
        self.min_patter = min_patter

    def check_input(self, min_patter: int, length: int) -> bool:
        valid = True
        if not isinstance(min_patter, int) or min_patter < 1:
            valid = False
        elif not isinstance(length, int) or length < min_patter * len(self.all_strings):
            valid = False
        return valid

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

    def run(self) -> None:
        whole_sample = string.ascii_lowercase
        whole_sample += string.ascii_uppercase
        whole_sample += string.digits
        whole_sample += string.punctuation
        mandatory = self.get_mandatory()
        length_left = self.length - len(mandatory)
        for _ in range(length_left):
            mandatory += secrets.choice(seq=whole_sample)
        self.display(mandatory)
