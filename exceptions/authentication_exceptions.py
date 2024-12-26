# Purpose: Define custom exceptions for configuration errors.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for authentication errors
class AuthenticationError(Exception):
	"""Base class for authentication exceptions."""
	def __init__(self, message: str) -> None:
		self.message = message
		super().__init__(self.message)

	def __str__(self) -> str:
		return f"{self.__class__.__name__}: {self.message}"


class InvalidCredentialsError(AuthenticationError):
	"""Exception raised for invalid credentials provided."""
	def __init__(self, account_type: str, message: str | None) -> None:
		base_message = f"Invalid {account_type} credentials."
		if message:
			base_message += f" {message}"
		super().__init__(base_message)

class AuthorizationError(AuthenticationError):
	"""Exception raised for unauthorized access."""
	def __init__(self, message: str | None) -> None:
		base_message = "User is not authorized to perform this action."
		if message:
			base_message += f" {message}"
		super().__init__(base_message)

class NoUserLoggedInError(AuthenticationError):
	"""Exception raised when no user is logged in."""
	def __init__(self, message: str | None) -> None:
		base_message = "Could retrieve current user id. No user is currently logged in."
		if message:
			base_message += f" {message}"
		super().__init__(base_message)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
