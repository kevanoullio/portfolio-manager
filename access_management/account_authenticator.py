# Purpose: Authentication module for authenticating user and validating credentials of various types.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries
import bcrypt

# Local modules imported for Type Checking purposes only
from database_management.database import Database
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

	def authenticate_user_credentials(self, provided_username: str, provided_password_bytes: bytes) -> bool:
		# Get the user account password hash
		user_account_password_hash: bytes | None = self.__user_account_operation.get_user_password_hash_by_username(provided_username)

		# Check if the provided password and the stored user account password match
		if user_account_password_hash is None:
			print("Username is in the database, but doesn't have an associated password.")
			return False

		# Verify the password
		if self.__authenticate_password(provided_password_bytes, user_account_password_hash):
			print("User account credentials authenticated successfully.")
			logging.info(f"User '{provided_username}' authenticated successfully.")
			return True
		else:
			print("Invalid user credentials.")
			return False

	def authenticate_email_credentials(self, provided_email_address: str, provided_password_bytes: bytes) -> bool:
		# TODO - put the commented out code in EmailAccountOperation
		# # Get an EmailAccount class based on the email
		# email_account: EmailAccount | None = self.email_account_operation.get_email_account_by_email_address(provided_email_address)
		# # Check if the email account exists.
		# if email_account is None:
		#     print("Email address is not in the database.")
		#     return None

		# Get the email account password hash
		email_account_password_hash: bytes | None = self.__email_account_operation.get_email_account_password_hash_by_email_address(provided_email_address)

		# Check if the email password exists.
		if email_account_password_hash is None:
			# If the email account was only added for notification purposes, the password hash will be None
			raise InvalidCredentialsError("email", "Email password hash is None.")

		# Validate the user's email credentials
		if self.__authenticate_password(provided_password_bytes, email_account_password_hash):
			print("Email account credentials authenticated successfully.")
			logging.info(f"Email '{provided_email_address}' authenticated successfully.")
			return True
		else:
			raise InvalidCredentialsError("email", None)

	def __authenticate_password(self, provided_password_bytes: bytes, stored_password_hash: bytes) -> bool:
		# Verify if the provided password matches the user's stored password
		return bcrypt.checkpw(provided_password_bytes, stored_password_hash)


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
