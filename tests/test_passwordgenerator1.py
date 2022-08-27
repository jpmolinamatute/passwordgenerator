import pytest

from password import PasswordGenerator

VALID_PASSWORD = ")lp]X&|}5/J~&M}-2=8W"


@pytest.fixture(name="password", scope="module")
def fixture_password() -> PasswordGenerator:
    return PasswordGenerator(min_pattern=2, length=20)


def test_has_min_digits_valid(password) -> None:
    valid = password.has_min_digits(VALID_PASSWORD)
    assert valid is True


def test_has_min_uppercase_valid(password) -> None:
    valid = password.has_min_uppercase(VALID_PASSWORD)
    assert valid is True


def test_has_min_lowercase_valid(password) -> None:
    valid = password.has_min_lowercase(VALID_PASSWORD)
    assert valid is True


def test_has_min_spe_char_valid(password) -> None:
    valid = password.has_min_spe_char(VALID_PASSWORD)
    assert valid is True


def test_validate_password_valid(password) -> None:
    valid = password.validate_password(VALID_PASSWORD)
    assert valid is True


def test_has_min_digits_invalid(password) -> None:
    invalid_password = "abcdefghijklmnopqrstuvwxyz"
    valid = password.has_min_digits(invalid_password)
    assert valid is False


def test_has_min_uppercase_invalid(password) -> None:
    invalid_password = "123456789"
    valid = password.has_min_uppercase(invalid_password)
    assert valid is False


def test_has_min_lowercase_invalid(password) -> None:
    invalid_password = "123456789"
    valid = password.has_min_lowercase(invalid_password)
    assert valid is False


def test_has_min_spe_char_invalid(password) -> None:
    invalid_password = "123456789"
    valid = password.has_min_spe_char(invalid_password)
    assert valid is False


def test_validate_password_invalid(password) -> None:
    invalid_password = "123456789"
    valid = password.validate_password(invalid_password)
    assert valid is False


def test_password_length(password) -> None:
    result = password.password()
    assert len(result) == 20
