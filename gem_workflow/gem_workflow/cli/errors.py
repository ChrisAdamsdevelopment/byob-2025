class ConfigMismatchError(Exception):
    """Raised when version locks do not match expected constants."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
