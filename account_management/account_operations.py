# Purpose: Account Operations module for performing CRUD operations on various account data types.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.database import Database
from user_interface.user_input import UserInput

# Local modules imported for Type Checking purposes only
from account_management.accounts import UserAccount, EmailAccount
from exceptions.authentication_exceptions import AuthenticationError

# Configure logging
import logging


# UserAccountOperation class for defining user account operations
class UserAccountOperation:
	def __init__(self, database: Database):
		self.__database = database

	def check_username_exists(self, provided_username: str) -> bool:
		result = self.__database.query_executor.get_user_account_by_username(provided_username)
		if result is None:
			return False
		return isinstance(result, UserAccount)

	# TODO - account for user roles for all methods that make changes to the database
	def create_user_account(self, provided_username: str, provided_password_hash: bytes) -> None:
		self.__database.query_executor.store_username_and_password(provided_username, provided_password_hash)

	def delete_user_account_from_database(self, user_account: UserAccount) -> None:
		# Delete the user's information from the database
		# Perform necessary database interactions to remove user data
		pass

	def get_user_account_by_user_id(self, provided_user_id: int) -> UserAccount | None:
		# Logic to retrieve user account from the database based on provided user_id
		# TODO - Implement this method and fix return
		return UserAccount(provided_user_id, "username")

	def get_user_account_by_username(self, provided_username: str) -> UserAccount | None:
		return self.__database.query_executor.get_user_account_by_username(provided_username)

	def get_user_password_hash_by_username(self, provided_username: str) -> bytes | None:
		return self.__database.query_executor.get_user_password_by_username(provided_username)

	def update_username(self, user_account: UserAccount, new_username: str) -> None:
		# Update the user's username to the new username
		user_account.username = new_username
		# TODO - finish this method

	def update_password(self, user_account: UserAccount, new_password_hash: bytes) -> None:
		# Update the user's password to the new password
		# user_account.username
		# user_account.user_id
		# new_password_hash
		pass
		# TODO - finish this method

	def deactivate_account(self, user_account: UserAccount) -> None:
		# Deactivate or disable the user's account
		# Perform any necessary cleanup or disable associated functionality
		pass

	def is_admin(self, user_account: UserAccount) -> bool:
		# Check if the user has admin privileges or roles
		# Return True if the user is an admin, False otherwise
		# TODO - Implement this method and fix return
		return False

	def get_user_profile(self, user_account: UserAccount) -> dict:
		# Retrieve and return the user's profile information
		# Return a dictionary containing profile data
		# TODO - Implement this method and fix return
		return {"username": user_account.username}


# EmailAccountOperation class for defining email account operations
class EmailAccountOperation:
	def __init__(self, database: Database):
		self.__database = database

	# TODO - finish this, should I do email_address or email_account???
	def check_email_address_exists(self, provided_email_address: str) -> bool:
		result = self.__database.query_executor.get_email_account_by_email_address(provided_email_address)
		logging.debug(f"check_email_address_exists() provided_email_address: {provided_email_address}")
		logging.debug(f"check_email_address_exists() result: {result}")

		if result is None:
			return False
		if isinstance(result, EmailAccount):
			return True
		else:
			return False

	def store_email_address_only(self, email_usage_id: int, provided_email_address: str) -> None:
		try:
			self.__database.query_executor.store_email_address_only(email_usage_id, provided_email_address)
		except AuthenticationError as e:
			print(f"Error storing email address: {e.message}")
			logging.warning(f"Error storing email address: {provided_email_address}. {e.message}")

	def store_email_address_and_password_hash(self, email_usage_id: int, provided_email_address: str, provided_password_hash: bytes) -> None:
		try:
			self.__database.query_executor.store_email_address_and_password_hash(email_usage_id, provided_email_address, provided_password_hash)
		except AuthenticationError as e:
			print(f"Error storing email address and password: {e.message}")
			logging.warning(f"Error storing email address and password: {provided_email_address}. {e.message}")

	def get_email_usage_names_by_email_address(self, provided_email_address: str) -> list[str] | None:
		try:
			return self.__database.query_executor.get_email_usage_names_by_email_address(provided_email_address)
		except AuthenticationError as e:
			print(f"Error getting email usage by email address: {e.message}")
			logging.warning(f"Error getting email usage by email address: {provided_email_address}. {e.message}")
			return None

	def get_email_account_password_hash_by_email_address(self, provided_email_address: str) -> bytes | None:
		# Check that the email address is in the database
		if not self.check_email_address_exists(provided_email_address):
			print("Email address is not in the database.")
			logging.debug(f"Email address is not in the database: {provided_email_address}")
			return None

		result = self.__database.query_executor.get_email_account_password_hash_by_email_address(provided_email_address)
		logging.debug(f"get_email_account_password_hash_by_email_address() provided_email_address: {provided_email_address}")
		return result

	# def import_data(self):
	#     # Logic to import data from the email account
	#     pass

	# def send_notification(self):
	#     # Logic to send a notification to the email account
	#     pass



	def add_email_account(self) -> int:
		if self.__database.session_manager.get_current_user() is None:
			print("You are not logged in.")
			return 1

		# Ask the user whether they want to add an email account for portfolio importing or for email notifications or both
		print("What would you like to use this email account for?")
		print("1. Portfolio Importing")
		print("2. Email Notifications")
		print("3. Both")
		print("4. Cancel")

		# Get the user's choice
		choice = UserInput.get_valid_menu_choice(4)

		# Check if the user wants to cancel
		if choice == 4:
			print("Email account import cancelled.")
			return 0

		# Get the email address from the user (email_prompt checks if it's valid)
		provided_email_address = UserInput.email_address_prompt()

		# Get the email usage from the provided email address
		try:
			email_usage_names = self.__database.query_executor.get_email_usage_names_by_email_address(provided_email_address)
		except AuthenticationError as e:
			raise e

		# Check if the email address is already in the database based on usage type
		if email_usage_names is not None:
			if choice == 1:
				if "import" in email_usage_names:
					print("Email address already in the database for portfolio importing.")
					return 2
			elif choice == 2:
				if "notification" in email_usage_names:
					print("Email address already in the database for notifications.")
					return 2
			elif choice == 3:
				if "import" in email_usage_names and "notification" in email_usage_names:
					print("Email address already in the database for both portfolio importing and notifications.")
					return 2

		# Get the email usage id by usage name
		import_id = self.__database.query_executor.get_email_usage_id_by_email_usage_name("import")
		notification_id = self.__database.query_executor.get_email_usage_id_by_email_usage_name("notification")

		# Check if the email usage id is None
		if import_id is None or notification_id is None:
			print("Error getting email usage id.")
			return 3

		# Only get the email password if the email usage is not "notification"
		if choice == 1:
			# Get the password from the user (password_prompt checks if it's valid)
			provided_email_password_hash: bytes = UserInput.password_prompt(prompt="Enter your email password: ", hash=True, confirm=True)
			self.store_email_address_and_password_hash(import_id, provided_email_address, provided_email_password_hash)
		elif choice == 2:
			self.store_email_address_only(notification_id, provided_email_address)
		elif choice == 3:
			# Get the password from the user (password_prompt checks if it's valid)
			provided_email_password_hash: bytes = UserInput.password_prompt(prompt="Enter your email password: ", hash=True, confirm=True)
			self.store_email_address_and_password_hash(import_id, provided_email_address, provided_email_password_hash)
			self.store_email_address_only(notification_id, provided_email_address)
		else:
			print("Invalid choice.")
			return 4

		print(f"Email account {provided_email_address} successfully added.")
		logging.info(f"Email account {provided_email_address} successfully added.")
		return 0


	def remove_email_account(self) -> int:
		if self.__database.session_manager.get_current_user() is None:
			print("You are not logged in.")
			return 1
		if self.__database.session_manager.get_current_user_id() is None:
			print("User id is None. Cannot remove email account.")
			return 1

		# Fetch all email addresses of usage "import" from the user
		email_accounts: list[EmailAccount] | None = self.__database.query_executor.get_all_current_user_email_accounts()
		logging.debug(f"Email accounts: {email_accounts}")

		# Check if any import email addresses are found
		if email_accounts is None or len(email_accounts) <= 0:
			print("No email accounts for found.")
			print("Please add an email account in the account settings.")
			return 1

		# Print the available email accounts
		title = "AVAILABLE EMAIL ACCOUNTS:"
		print(f"\n{title}")
		for i, email_account in enumerate(email_accounts, start=1):
			print(f"{i}: {email_account.address}")

		# Initialize the UserInput class
		user_input = UserInput()

		# Get the user's choice
		choice = user_input.get_valid_menu_choice(len(email_accounts), "Choose the email account you would like to delete: ")
		# Get the email account based on the user's choice
		selected_email_account = email_accounts[choice - 1]
		logging.debug(f"Selected email account: {selected_email_account}")

		# Check that the email address is in the database
		if not self.__database.query_executor.entry_exists(
				"email",
				"address",
				selected_email_account.address,
				self.__database.session_manager.get_current_user_id()):
			print("Email address is not in the database.")
			return 2

		# Prep the email information for deletion into the database
		columns = ("address",)
		values = (selected_email_account.address,)

		# Delete the entry from the database
		try:
			self.__database.query_executor.delete_entry("email", columns, values, self.__database.session_manager.get_current_user_id())
		except Exception as e:
			print("Error deleting email account from the database.")
			logging.warning(e)
			return 3

		print("Email account successfully removed.")
		logging.info(f"Email account {selected_email_account.address} successfully removed.")
		return 0


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
