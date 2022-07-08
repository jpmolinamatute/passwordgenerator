from .passwordgenerator import PasswordGenerator


def main() -> None:
    generate = PasswordGenerator()
    generate.display()


if __name__ == "__main__":
    main()
