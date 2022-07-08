class PasswordException(Exception):
    def __init__(self, *args: object) -> None:
        self.message = args[0] if args else ""
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Error: {self.message}"
