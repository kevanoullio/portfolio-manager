# Purpose: User Input module for sanitizing and validating all user input.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules

# Configure logging
import logging
from config import configure_logging
configure_logging()


# Generic Validator class for validating values
class Validator:
    def __init__(self, minimum_length: int, maximum_length: int, allowed_characters: str, valid_form: str) -> None:
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length
        self.allowed_characters = allowed_characters
        self.valid_form = valid_form


    def __is_valid_length(self, value: str) -> bool:
        return self.minimum_length <= len(value) <= self.maximum_length


    def __is_valid_characters(self, value: str) -> bool:
        return re.match(f"^[{self.allowed_characters}]*$", value) is not None
    

    def __is_valid_form(self, value: str) -> bool:
        return re.match(self.valid_form, value) is not None


    def validate(self, value: str) -> bool:
        return self.__is_valid_length(value) and self.__is_valid_characters(value) and self.__is_valid_form(value)


# UsernameValidator class for validating usernames
class UsernameValidator(Validator):
    def __init__(self, minimum_length: int = 4, maximum_length: int = 32) -> None:
        allowed_characters = r"a-zA-Z0-9_"
        valid_username_form = r"^[a-zA-Z0-9_]*$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_username_form)


    def validate_username(self, username: str) -> bool:
        # Validates the provided username
        if not self.validate(username):
            return False
        return True
    

# PasswordValidator class for validating passwords
class PasswordValidator(Validator):
    def __init__(self, minimum_length: int = 3, maximum_length: int = 64):
        allowed_characters = r"a-zA-Z0-9_"
        valid_password_form = r"^[a-zA-Z0-9_]*$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_password_form)


    def validate_password(self, password: str) -> bool:
        # Validates the provided password
        if not self.validate(password):
            return False
        return True


# EmailValidator class for validating emails
class EmailValidator(Validator):
    def __init__(self, minimum_length: int = 6, maximum_length: int = 254):
        allowed_characters = r"a-zA-Z0-9_@.-"
        valid_email_form = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        super().__init__(minimum_length, maximum_length, allowed_characters, valid_email_form)
    
        
    def validate_email(self, email: str) -> bool:
        # Validates the provided email address
        if not self.validate(email):
            return False
        return True


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


    def __hash_password(self, password: bytes) -> bytes:
        # Salt the password for extra security
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password


    def username_prompt(self, prompt: str = "Enter your username: ",) -> str:
        # Get the username from the user
        provided_username = input(prompt)

        # Check if the provided username is valid
        while not self.username_validator.validate_username(provided_username):
            print("Invalid username. Only alphanumeric characters and underscores are allowed.")
            provided_username = input("Please try again: ")

        # Sanitize the provided username
        provided_username = self.__sanitize_input(provided_username)

        return provided_username


    def password_prompt(self, prompt: str = "Enter your password: ", confirm: bool = False, confirm_prompt: str = "Confirm your password: ") -> bytes:
        # Get the password from the user
        provided_password = getpass(prompt)

        # Check if the provided password is valid
        while not self.password_validator.validate_password(provided_password):
            print("Invalid password. Only alphanumeric characters and underscores are allowed.")
            provided_password = getpass("Please try again: ")

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
