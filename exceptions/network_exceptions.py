# Purpose: Define custom exceptions for database errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for network errors
class NetworkError(Exception):
    """Base class for network exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class TimeoutError(NetworkError):
    def __init__(self):
        self.message = "Network operation timed out."
        super().__init__(self.message)

class NetworkConnectionError(NetworkError):
    def __init__(self):
        self.message = "Failed to connect to the network."
        super().__init__(self.message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
