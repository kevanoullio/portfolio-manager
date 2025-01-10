# Purpose: User Input module for sanitizing and validating all user input.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules
from exceptions.validation_exceptions import ValidationError, LengthError, CharacterError, FormError

# Configure logging
import logging


# Generic Validator class with static methods for validating values
class Validator:
	@staticmethod
	def __is_valid_length(value: str, minimum_length: int, maximum_length: int) -> bool:
		return minimum_length <= len(value) <= maximum_length

	@staticmethod
	def __is_valid_characters(value: str, allowed_characters: str) -> bool:
		return re.match(f"^[{allowed_characters}]*$", value) is not None

	@staticmethod
	def __is_valid_form(value: str, valid_form: str) -> bool:
		return re.match(valid_form, value) is not None

	@staticmethod
	def validate(type: str, value: str, minimum_length: int, maximum_length: int, allowed_characters: str, valid_form: str) -> None:
		if not Validator.__is_valid_length(value, minimum_length, maximum_length):
			raise LengthError(type, minimum_length, maximum_length)

		if not Validator.__is_valid_characters(value, allowed_characters):
			raise CharacterError(type)

		if not Validator.__is_valid_form(value, valid_form):
			raise FormError(type)


# ValidationConfig class for storing validation configurations
class ValidationConfig:
	USERNAME = {
		"minimum_length": 3,
		"maximum_length": 32,
		"allowed_characters": r"a-zA-Z0-9_",
		"valid_form": r"^[a-zA-Z0-9_]*$"
	}
	PASSWORD = {
		"minimum_length": 3,
		"maximum_length": 64,
		"allowed_characters": r"a-zA-Z0-9_!@#$%^&*()-_=+`~\[{\]}\\|:,./?",
		"valid_form": r"^[a-zA-Z0-9_!@#$%^&*()-_=+`~\[{\]}\\|:,./?]+$"
	}
	EMAIL = {
		"minimum_length": 6,
		"maximum_length": 254,
		"allowed_characters": r"a-zA-Z0-9_@.-",
		"valid_form": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
	}


# UserInput class for sanitizing and validating user input
class UserInput:
	@staticmethod
	def __hash_password(provided_password: bytes) -> bytes:
		# Salt the provided password for extra security
		salt = bcrypt.gensalt()
		return bcrypt.hashpw(provided_password, salt)

	@staticmethod
	def sanitize_input(raw_input: str) -> str:
		# Remove any potentially dangerous characters that can lead to SQL injection or XSS or other attacks
		return raw_input.translate(str.maketrans('', '', '\'"<>;'))

	@staticmethod
	def username_prompt(prompt: str = "Enter your username: ") -> str:
		while True:
			provided_username = input(prompt)
			try:
				Validator.validate("Username", provided_username, **ValidationConfig.USERNAME) # ** unpacks the dictionary
				return UserInput.sanitize_input(provided_username)
			except ValidationError as e:
				logging.warning(f"Invalid username: {provided_username}. {e.message}")
				print(f"Invalid username. {e.message}")

	@staticmethod
	def password_prompt(prompt: str = "Enter your password: ", hash: bool = False, confirm: bool = False, confirm_prompt: str = "Confirm your password: ") -> bytes:
		"""
		This function prompts the user for a password and ensures that it is a valid password format.

		Args:
			prompt (str): The desired prompt to display to the user.
			confirm (bool): Whether or not to confirm the provided password with a second prompt.
			confirm_prompt (str): The desired prompt to display to the user for confirming the password.

		Returns:
			(bytes): If confirm is set to False, this function returns the hashed password as bytes, otherwise it returns the provided password as bytes without hashing.
		"""
		while True:
			# Get the password from the user
			provided_password = getpass(prompt)

			try:
				# Validate the provided password
				Validator.validate("Password", provided_password, **ValidationConfig.PASSWORD) # ** unpacks the dictionary
				break
			except ValidationError as e:
				text: str = f"Invalid password. {e.message}"
				print(text)
				logging.warning(text)

		# Confirm the provided password if confirm was set to True
		if confirm:
			while True:
				confirm_password = getpass(confirm_prompt)
				if provided_password != confirm_password:
					print("Passwords do not match. Please try again.")
					continue
				break

		# Convert the password to bytes
		encoded_password = provided_password.encode()

		if hash:
			return UserInput.__hash_password(encoded_password)
		else:
			return encoded_password

	@staticmethod
	def email_address_prompt(prompt: str = "Enter your email address: ") -> str:
		while True:
			provided_email = input(prompt)
			try:
				Validator.validate("Email", provided_email, **ValidationConfig.EMAIL) # ** unpacks the dictionary
				return UserInput.sanitize_input(provided_email)
			except ValidationError as e:
				logging.warning(f"Invalid email address: {provided_email}. {e.message}")
				print(f"Invalid email address. {e.message}")

	@staticmethod
	def get_valid_menu_choice(maximum_choice: int, choice_prompt: str = "Please enter your choice: ") -> int:
		while True:
			choice = input(f"\n{choice_prompt}")

			# Check if the input is a digit
			if not choice.isdigit():
				print("Invalid input. Please enter a digit.")
				continue

			# Cast the input to an integer
			choice = int(choice)

			# Check if the input is within the valid range
			logging.debug(f"Choice: {choice}")
			logging.debug(f"Maximum choice: {maximum_choice}")
			if choice < 0 or choice > maximum_choice:
				print("Invalid input. Please enter a valid option.")
				continue

			return choice


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
