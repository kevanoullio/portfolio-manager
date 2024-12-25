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


# Generic Validator class for validating values
class Validator:
    def __init__(self, minimum_length: int, maximum_length: int, allowed_characters: str, valid_form: str) -> None:
        self.__minimum_length = minimum_length
        self.__maximum_length = maximum_length
        self.__allowed_characters = allowed_characters
        self.__valid_form = valid_form

    def __is_valid_length(self, value: str) -> bool:
        return self.__minimum_length <= len(value) <= self.__maximum_length

    def __is_valid_characters(self, value: str) -> bool:
        return re.match(f"^[{self.__allowed_characters}]*$", value) is not None

    def __is_valid_form(self, value: str) -> bool:
        return re.match(self.__valid_form, value) is not None

    def validate(self, value: str) -> None:
        # Validate the length of the provided input
        if not self.__is_valid_length(value):
            raise LengthError(self.__minimum_length, self.__maximum_length)

		# Validate the characters of the provided input
        if not self.__is_valid_characters(value):
            raise CharacterError()

		# Validate the form of the provided input
        if not self.__is_valid_form(value):
            raise FormError()


# UsernameValidator class for validating usernames
class UsernameValidator(Validator):
    def __init__(self, minimum_length: int = 3, maximum_length: int = 32) -> None:
        allowed_characters = r"a-zA-Z0-9_"
        valid_username_form = r"^[a-zA-Z0-9_]*$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_username_form)


# PasswordValidator class for validating passwords
class PasswordValidator(Validator):
    def __init__(self, minimum_length: int = 3, maximum_length: int = 64) -> None:
        # Allow all special characters except for single quote, double quote, less than, greater than, and semicolon
        allowed_characters = r"a-zA-Z0-9_!@#$%^&*()-_=+`~\[{\]}\\|:,./?"
        valid_password_form = r"^[a-zA-Z0-9_!@#$%^&*()-_=+`~\[{\]}\\|:,./?]+$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_password_form)
        # Allow all special characters except for single quote, double quote, less than, greater than, and semicolon

# EmailValidator class for validating emails
class EmailAddressValidator(Validator):
    def __init__(self, minimum_length: int = 6, maximum_length: int = 254) -> None:
        allowed_characters = r"a-zA-Z0-9_@.-"
        valid_email_form = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_email_form)


# UserInput class for sanitizing and validating all user input
class UserInput:
    def __init__(self) -> None:
        self.__username_validator = UsernameValidator()
        self.__password_validator = PasswordValidator()
        self.__email_validator = EmailAddressValidator()

    def __sanitize_input(self, raw_input: str) -> str:
        # Remove any potentially dangerous characters that can lead to SQL injection or XSS or other attacks
        sanitized_input = raw_input.translate(str.maketrans('', '', '\'"<>;'))
        return sanitized_input

    def __hash_password(self, provided_password: bytes) -> bytes:
        # Salt the provided password for extra security
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(provided_password, salt)
        return hashed_password

    def username_prompt(self, prompt: str="Enter your username: ") -> str:
            while True:
                # Get the username from the user
                provided_username = input(prompt)

                try:
                    # Validate the provided username
                    self.__username_validator.validate(provided_username)
                    # Sanitize the provided username
                    provided_username = self.__sanitize_input(provided_username)
                    return provided_username
                except ValidationError as e:
                    print(f"Invalid username. {e.message}")

    def password_prompt(self, prompt: str="Enter your password: ", confirm: bool=False, confirm_prompt: str="Confirm your password: ") -> bytes:
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
                self.__password_validator.validate(provided_password)
                break
            except ValidationError as e:
                print(f"Invalid password. {e.message}")

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

        if confirm:
            # If confirm is True, hash the password (bytes) and return it as bytes
            return self.__hash_password(encoded_password)
        else:
            # If confirm is False, don't hash the password and return it as bytes
            return encoded_password

    def email_address_prompt(self, prompt: str="Enter your email address: ") -> str:
        while True:
            # Get the email address from the user
            provided_email = input(prompt)

            try:
                # Validate the provided email address
                self.__email_validator.validate(provided_email)
                # Sanitize the provided email address
                provided_email = self.__sanitize_input(provided_email)
                return provided_email
            except ValidationError as e:
                print(f"Invalid email address. {e.message}")

    def get_valid_menu_choice(self, maximum_choice: int, choice_prompt: str | None="Please enter your choice: ") -> int:
        while True:
            choice = input(f"\n{choice_prompt}")

            # Check if the input is a digit
            if not choice.isdigit():
                print("Invalid input. Please enter a digit.")
                continue

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
