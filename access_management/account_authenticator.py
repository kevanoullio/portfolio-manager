# Purpose: Authentication module for authenticating user and validating credentials of various types.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries
import bcrypt

# Local Modules

# Local modules imported for Type Checking purposes only
from database_management.database import Database
from user_interface.user_input import UserInput
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from exceptions.authentication_exceptions import InvalidCredentialsError

# Configure logging
import logging


# Authentication class for authenticating user and validating credentials of various types
class AccountAuthenticator:
	def __init__(self, database: Database) -> None:
		self.__database = database
		self.__user_account_operation = UserAccountOperation(self.__database)
		self.__email_account_operation = EmailAccountOperation(self.__database)
		logging.debug("UserAuthentication initialized.")

	def authenticate_user_credentials(self, provided_username: str) -> bool:
		# Prompt the user for the user account password
		provided_password_hash = UserInput.password_prompt(prompt="Verify your user account credentials by entering your user account password: ", confirm=False)

		# Get the user account password hash
		user_account_password_hash: bytes | None = self.__user_account_operation.get_user_password_hash_by_username(provided_username)

		# Check if the provided password and the stored user account password match
		if user_account_password_hash is None:
			print("Username is in the database, but doesn't have an associated password.")
			return False

		# Verify the password
		if self.__authenticate_password(provided_password_hash, user_account_password_hash):
			print("User account authenticated.")
			return True
		else:
			print("Invalid user credentials.")
			return False

	def authenticate_email_credentials(self, provided_email_address: str) -> bool:
		# TODO - put the commented out code in EmailAccountOperation
		# # Get an EmailAccount class based on the email
		# email_account: EmailAccount | None = self.email_account_operation.get_email_account_by_email_address(provided_email_address)
		# # Check if the email account exists.
		# if email_account is None:
		#     print("Email address is not in the database.")
		#     return None

		# Prompt the user for the email account password
		provided_password_hash = UserInput.password_prompt(prompt="Verify your email credentials by entering your email password: ", confirm=False)

		# Get the email account password hash
		email_account_password_hash: bytes | None = self.__email_account_operation.get_email_account_password_hash_by_email_address(provided_email_address)

		# Check if the email password exists.
		if email_account_password_hash is None:
			# If the email account was only added for notification purposes, the password hash will be None
			raise InvalidCredentialsError("email", "Email password hash is None.")

		# Validate the user's email credentials
		if self.__authenticate_password(provided_password_hash, email_account_password_hash):
			print("Email account authenticated.")
			return True
		else:
			raise InvalidCredentialsError("email", None)

	def __authenticate_password(self, provided_password_hash: bytes, stored_password_hash: bytes) -> bool:
		# Verify if the provided password matches the user's stored password
		result = bcrypt.checkpw(provided_password_hash, stored_password_hash)
		return result


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
