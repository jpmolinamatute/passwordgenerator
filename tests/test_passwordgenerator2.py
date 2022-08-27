import pytest

from password import PasswordGenerator, PasswordGeneratorException


def test_raises_exception_when_length_0():
    with pytest.raises(PasswordGeneratorException):
        PasswordGenerator(min_pattern=2, length=0)


def test_raises_exception_when_min_0():
    with pytest.raises(PasswordGeneratorException):
        PasswordGenerator(min_pattern=0, length=20)
