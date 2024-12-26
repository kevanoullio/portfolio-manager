# Purpose: Define custom exceptions for configuration errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for configuration errors
class ConfigurationError(Exception):
    """Base class for configuration exceptions."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class InvalidConfigurationError(ConfigurationError):
    def __init__(self):
        self.message = "Invalid configuration settings."
        super().__init__(self.message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
