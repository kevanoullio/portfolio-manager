# Purpose: Define custom exceptions for data validation errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for data validation errors
class DataValidationError(Exception):
    """Base class for data validation exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidDataError(DataValidationError):
    def __init__(self):
        self.message = "Invalid data provided."
        super().__init__(self.message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
