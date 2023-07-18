# Purpose: Email Account module for defining email account data type and its associated functionality.

# Standard Libraries
from dataclasses import dataclass

# Third-party Libraries

# Local Modules
from data_management.connection import DatabaseConnection

# Configure logging
import logging


# EmailAccount class for defining email account data type
@dataclass
class EmailAccount:
    usage: str
    address: str
    password_hash: bytes | None = None

    def __post_init__(self) -> None:
        logging.info(f"Email account initialized successfully. Address: {self.address}, Usage: {self.usage}")


class EmailAccountService:
    def __init__(self, database_connection: DatabaseConnection):
        self.database_connection = database_connection

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
