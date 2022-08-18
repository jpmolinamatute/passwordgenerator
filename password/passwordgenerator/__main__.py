from .passwordgenerator import PasswordGenerator


def main() -> None:
    password = PasswordGenerator()
    password.display()


if __name__ == "__main__":
    main()
