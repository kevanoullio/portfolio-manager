# Purpose: User Input module for sanitizing and validating all user input.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules

# Configure logging
import logging


# Generic Validator class for validating values
class Validator:
    def __init__(self, minimum_length: int, maximum_length: int, allowed_characters: str, valid_form: str) -> None:
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.allowed_characters = allowed_characters
        self.valid_form = valid_form


    def is_valid_length(self, value: str) -> bool:
        return self.minimum_length <= len(value) <= self.maximum_length


    def is_valid_characters(self, value: str) -> bool:
        return re.match(f"^[{self.allowed_characters}]*$", value) is not None
    

    def is_valid_form(self, value: str) -> bool:
        return re.match(self.valid_form, value) is not None


    def validate(self, value: str) -> int:
        # Validate the length of the provided username
        if not self.is_valid_length(value):
            return 1
        
        # Validate the characters of the provided username
        if not self.is_valid_characters(value):
            return 2
        
        # Validate the form of the provided username
        if not self.is_valid_form(value):
            return 3

        # All checks completed, provided username is valid
        return 0


# UsernameValidator class for validating usernames
class UsernameValidator(Validator):
    def __init__(self, minimum_length: int = 3, maximum_length: int = 32) -> None:
        allowed_characters = r"a-zA-Z0-9_"
        valid_username_form = r"^[a-zA-Z0-9_]*$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_username_form)
    

# PasswordValidator class for validating passwords
class PasswordValidator(Validator):
    def __init__(self, minimum_length: int = 3, maximum_length: int = 64) -> None:
        allowed_characters = r"a-zA-Z0-9_"
        valid_password_form = r"^[a-zA-Z0-9_]*$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_password_form)


# EmailValidator class for validating emails
class EmailValidator(Validator):
    def __init__(self, minimum_length: int = 6, maximum_length: int = 254) -> None:
        allowed_characters = r"a-zA-Z0-9_@.-"
        valid_email_form = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_email_form)


# UserInput class for sanitizing and validating all user input
class UserInput:
    def __init__(self) -> None:
        self.username_validator = UsernameValidator()
        self.password_validator = PasswordValidator()
        self.email_validator = EmailValidator()


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
        # Get the username from the user
        provided_username = input(prompt)

        # Check if the provided username is valid
        while self.username_validator.validate(provided_username) != 0:
            print("Invalid username. ", end="")
            if self.username_validator.validate(provided_username) == 1:
                print(f"Must be between {self.username_validator.minimum_length} and {self.username_validator.maximum_length} characters long.")
            elif self.username_validator.validate(provided_username) == 2:
                print("Only alphanumeric characters and underscores are allowed.")
            elif self.username_validator.validate(provided_username) == 3:
                print("Must only contain alphanumeric characters and underscores with no separations.")
            provided_username = input("Please try again: ")

        # Sanitize the provided username
        provided_username = self.__sanitize_input(provided_username)

        return provided_username


    def password_prompt(self, prompt: str="Enter your password: ", confirm: bool=False, confirm_prompt: str="Confirm your password: ") -> bytes:
        # Get the password from the user
        provided_password = getpass(prompt)

        # Check if the provided password is valid
        while self.username_validator.validate(provided_password) != 0:
            print("Invalid password. ", end="")
            if self.username_validator.validate(provided_password) == 1:
                print(f"Must be between {self.password_validator.minimum_length} and {self.password_validator.maximum_length} characters long.")
            elif self.username_validator.validate(provided_password) == 2:
                print("Only alphanumeric characters and underscores are allowed.")
            elif self.username_validator.validate(provided_password) == 3:
                print("Must only contain alphanumeric characters and underscores with no separations.")
            provided_password = input("Please try again: ")

        # Confirm the provided password if confirm was set to True
        if confirm:
            while True:
                confirm_password = getpass(confirm_prompt)
                if provided_password != confirm_password:
                    print("Passwords do not match. Please try again.")
                    continue
                break
        
        # Sanitize the provided password
        provided_password = self.__sanitize_input(provided_password)

        # Convert the password to bytes
        encoded_password = provided_password.encode()

        if confirm:
            # If confirm is True, hash the password (bytes) and return it as bytes
            return self.__hash_password(encoded_password)
        else:
            # If confirm is False, don't hash the password and return it as bytes
            return encoded_password


    def email_prompt(self, prompt: str="Enter your email address: ") -> str:
        # Get the email address from the user
        provided_email = input(prompt)

        # Check if the provided email address is valid
        while self.email_validator.validate(provided_email) != 0:
            print("Invalid email address. ", end="")
            if self.email_validator.validate(provided_email) == 1:
                print(f"Must be between {self.email_validator.minimum_length} and {self.email_validator.maximum_length} characters long.")
            elif self.email_validator.validate(provided_email) == 2:
                print("Only alphanumeric characters, underscores, periods, hyphens, and @ symbols are allowed.")
            elif self.email_validator.validate(provided_email) == 3:
                print("Must be in the form of a standard email address, i.e. 'email@service.something'")

        # Sanitize the provided email address
        provided_email = self.__sanitize_input(provided_email)

        return provided_email


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
