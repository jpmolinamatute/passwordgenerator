from .passwordgenerator import PasswordGenerator


def main() -> None:
    password = PasswordGenerator()
    password.display()
    password.destroy()


if __name__ == "__main__":
    main()
