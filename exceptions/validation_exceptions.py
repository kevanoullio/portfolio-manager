# Purpose:

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging


# Custom Exception for Validation Errors
class ValidationError(Exception):
	"""Base class for validation errors."""
	def __init__(self, message: str) -> None:
		self.message = message
		super().__init__(self.message)


class LengthError(ValidationError):
	"""Exception for length errors."""
	def __init__(self, minimum_length, maximum_length):
		self.message = f"Must be between {minimum_length} and {maximum_length} characters long."
		super().__init__(self.message)

class CharacterError(ValidationError):
	"""Exception for character errors."""
	def __init__(self):
		self.message = "Contains invalid characters."
		super().__init__(self.message)

class FormError(ValidationError):
	"""Exception for form errors."""
	def __init__(self):
		self.message = "Does not match the required form."
		super().__init__(self.message)
