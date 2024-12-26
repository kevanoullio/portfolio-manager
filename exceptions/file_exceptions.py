# Purpose: Define custom exceptions for file handling errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for file handling errors
class FileError(Exception):
    """Base class for file handling exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class FileNotFoundError(FileError):
    def __init__(self):
        self.message = "File not found."
        super().__init__(self.message)

class FileReadError(FileError):
    def __init__(self):
        self.message = "Failed to read the file."
        super().__init__(self.message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
