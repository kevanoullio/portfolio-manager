# Purpose: Account Operations module for performing methods and operations on various account data types.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.database import Database

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount

# Configure logging
import logging


# UserAccountOperation class for defining user account operations
class UserAccountOperation:
    def __init__(self, database: Database):
        self._database = database

    def check_username_exists(self, provided_username: str) -> bool:
        result = self._database.query_executor.get_user_account_by_username(provided_username)
        if result is None:
            return False
        if isinstance(result, UserAccount):
            return True
        else:
            return False

    # TODO - account for user roles for all methods that make changes to the database
    def save_username_and_password_to_database(self, username: str, password: bytes) -> None:
        # Save the user's information to the database
        # Perform necessary database interactions to store user data
        pass

    def delete_user_account_from_database(self, user_account: UserAccount) -> None:
        # Delete the user's information from the database
        # Perform necessary database interactions to remove user data
        pass

    def get_user_account_by_user_id(self, provided_user_id: int) -> UserAccount | None:
        # Logic to retrieve user account from the database based on provided user_id
        # TODO - Implement this method and fix return
        return UserAccount(provided_user_id, "username")
    
    def get_user_account_by_username(self, provided_username: str) -> UserAccount | None:
        return self._database.query_executor.get_user_account_by_username(provided_username)
    
    def get_user_password_by_username(self, provided_username: str) -> bytes | None:
        return self._database.query_executor.get_user_password_by_username(provided_username)

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
        self._database = database

    # TODO - finish this, should I do email_address or email_account???
    # def check_email_address_exists(self, provided_email_address: str) -> bool:
    #     result = self.query_executor.get_user_account_by_username(provided_email_address)
    #     if result is None:
    #         return False
    #     if isinstance(result, UserAccount):
    #         return True
    #     else:
    #         return False

    def get_email_usage_by_email_address(self, provided_email_address: str) -> list[str] | None:
        return self._database.query_executor.get_email_usage_by_email_address(provided_email_address)

    def get_email_password_by_email_address(self, provided_email_address: str) -> bytes | None:
        # TODO - finish this method
        pass

    # def import_data(self):
    #     # Logic to import data from the email account
    #     pass

    # def send_notification(self):
    #     # Logic to send a notification to the email account
    #     pass



    # def add_email_account(self, email_usage: str) -> int:
    #     if self.session_manager.current_user is None:
    #         print("You are not logged in.")
    #         return 1

    #     # Get the email address from the user (email_prompt checks if it's valid)
    #     provided_email = self.user_input.email_prompt()

    #     # Get the email_usage_id from the database
    #     email_usage_id = self.query_executor.get_email_usage_id(email_usage)

    #     # Check if the email address is already in the database
    #     if self.query_executor.entry_exists("email",
    #             f"email_address='{provided_email}' AND email_usage_id='{email_usage_id}'",
    #             self.session_manager.current_user.user_id):
    #         print("Email address already in the database.")
    #         return 2
        
    #     # Only get the email password if the email usage is not "notification"
    #     if email_usage == "notification":
    #         provided_password = None
    #         # Prep the email information for insertion into the database
    #         columns = ("email_address", "email_usage_id")
    #         values = (provided_email, email_usage_id)
    #     else:
    #         # Get the password from the user (password_prompt checks if it's valid)
    #         provided_password = self.user_input.password_prompt(prompt="Enter your email password", confirm=True)
    #         # Prep the email information for insertion into the database
    #         columns = ("email_address", "password_hash", "email_usage_id")
    #         values = (provided_email, provided_password, email_usage_id)
        
    #     # Insert the entry into the database
    #     try:
    #         self.query_executor.insert_entry("email", columns, values, self.session_manager.current_user.user_id)
    #         # Add the email account to the current user
    #         self.session_manager.current_user.add_email_account(EmailAccount(email_usage, provided_email, provided_password))
    #     except Exception as e:
    #         print("Error inserting email account into the database.")
    #         logging.warning(e)
    #         return 3

    #     print("Email account import successful.")
    #     return 0


    # def remove_email_account(self, email_usage: str) -> int:
    #     if self.session_manager.current_user is None:
    #         print("You are not logged in.")
    #         return 1
    #     # if self.session_manager.current_user.user_id is None:
    #     #     print("User id is None. Cannot remove email account.")
    #     #     return 1
    
    #     # Get the email address from the user (email_prompt checks if it's valid)
    #     provided_email = self.user_input.email_prompt()

    #     # Get the email_usage_id from the database
    #     email_usage_id = self.query_executor.get_email_usage_id(email_usage)

    #     # Check that the email address is in the database
    #     if not self.query_executor.entry_exists("email",
    #             f"email_address='{provided_email}' AND email_usage_id='{email_usage_id}'",
    #             self.session_manager.current_user.user_id):
    #         print("Email address is not in the database.")
    #         return 2

    #     # Only get the email password if the email usage is not "notification"
    #     if email_usage == "notification":
    #         provided_password = None
    #         # Prep the email information for insertion into the database
    #         columns = ("email_address", "email_usage_id")
    #         values = (provided_email, email_usage_id)
    #     else:
    #         # Get the password from the user (password_prompt checks if it's valid)
    #         provided_password = self.user_input.password_prompt(prompt="Enter your email password", confirm=True)
    #         # Verify the email password
    #         if not self.validate_email_credentials(provided_email, provided_password):
    #             print("Invalid email credentials.")
    #             return 2
    #         # Prep the email information for insertion into the database
    #         columns = ("email_address", "password_hash", "email_usage_id")
    #         values = (provided_email, provided_password, email_usage_id)
        
    #     # Delete the entry from the database
    #     try:
    #         self.query_executor.delete_entry("email", columns, values, self.session_manager.current_user.user_id)
    #         # Remove the email account from the current user
    #         self.session_manager.current_user.remove_email_account(EmailAccount(email_usage, provided_email, provided_password))
    #     except Exception as e:
    #         print("Error deleting email account from the database.")
    #         logging.warning(e)
    #         return 3
        
    #     print("Email account successfully removed.")
    #     return 0


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
