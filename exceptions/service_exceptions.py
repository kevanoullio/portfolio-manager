# Purpose: Define custom exceptions for configuration errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for service errors
class ServiceError(Exception):
    """Base class for service exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ServiceUnavailableError(ServiceError):
    def __init__(self):
        self.message = "Service is currently unavailable."
        super().__init__(self.message)

class RateLimitExceededError(ServiceError):
    def __init__(self):
        self.message = "Rate limit exceeded."
        super().__init__(self.message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
