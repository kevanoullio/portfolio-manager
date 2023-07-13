# Purpose: Authentication module for authenticating users and managing user accounts.

# Standard Libraries

import re

# Third-party Libraries
import bcrypt

# Local Modules
from user_authentication.user import EmailAccount, User
from data_management.queries import QueryExecutor
from session.session_manager import SessionManager

# Configure logging
import logging
from config import configure_logging
configure_logging()

# Start using logging
logging.debug("This is a debug message.")


# UserAuthentication class for managing user authentication
class UserAuthentication:
    def __init__(self, session_manager: SessionManager, query_executor: QueryExecutor):
        self.session_manager = session_manager
        self.query_executor = query_executor


    def authenticate_user(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Check if the provided credentials are valid
        if self.validate_credentials(provided_username, provided_password_hash):
            # Perform additional checks or actions if needed
            print("Login successful!")
            return True
        else:
            print("Account login failed. Please try again.")
            return False


    def validate_credentials(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Get a User class based on the username
        user = self.query_executor.get_user_by_username(provided_username)
        # Check if the user exists and the password matches
        if user and user.verify_password(provided_password_hash):
            return True
        else:
            print("Invalid credentials.")
            return False


    def get_user_by_username(self, provided_username: str) -> User | None:
        user = self.query_executor.get_user_by_username(provided_username)
        return user


    def generate_session_token(self, user_id):
        # Generate a session token for the user
        # This can involve creating a unique token, associating it with the user ID,
        # and storing it in the database or an in-memory cache
        # Return the generated session token
        pass

    def verify_session_token(self, session_token):
        # Verify the validity of the session token
        # Check if the session token is present in the database or cache
        # Return True if the token is valid, False otherwise
        pass

    def clear_session_token(self, session_token):
        # Remove the session token from the database or cache
        pass











    # def modify_account(self):
    #     print("Modifying the account...")
    #     # Code for modifying the account
    #     # Example: Use a third-party library or API to modify the account
    #     print("Account modification successful.")


    # def delete_account(self):
    #     print("Deleting the account...")
    #     # Code for deleting the account
    #     # Example: Use a third-party library or API to delete the account
    #     print("Account deletion successful.")
    #     # Unload the user id of the deleted account



    # def import_email_account(self, database: Database, email_usage: str) -> int:
    #     if self.session_manager.current_user is None:
    #         print("You are not logged in.")
    #         return 1
    #     if self.session_manager.current_user.user_id is None:
    #         print("User id is None. Cannot import email account.")
    #         return 1

    #     # Get the email address from the user
    #     email = input("Please enter the email address: ")
    #     # TODO - Check if the email is valid using third-party service?
    #     while not self.is_valid_email(email):
    #         print("Invalid email address, please try again. ", end="")
    #         email = input()

    #     # Sanitize the email address
    #     email = self.__sanitize_input(email)

    #     # Get the email_usage_id from the database
    #     email_usage_id = database.query_executor.get_email_usage_id(email_usage)

    #     # Check if the email address is already in the database
    #     if database.query_executor.entry_exists("email",
    #             f"email_address='{email}' AND email_usage_id='{email_usage_id}'",
    #             self.session_manager.current_user.user_id):
    #         print("Email address already in database.")
    #         return 2
        
    #     # Get the password from the user
    #     password = self.__password_input("Please enter the email password: ")

    #     if password is None:
    #         print("Account login failed. Password is None.")
    #         return 3

    #     # Add all the information to the database
    #     columns = ("email_address", "password_hash", "email_usage_id")
    #     values = (email, password, email_usage_id)
        
    #     # Insert the entry into the database
    #     database.insert_entry("email", columns, values, self.session_manager.current_user.user_id)
    #     print("Email account import successful.")
    #     return 0


    # def remove_email_account(self, database: Database, email_usage: str) -> int:
    #     if self.session_manager.current_user is None:
    #         print("You are not logged in.")
    #         return 1
    #     if self.session_manager.current_user.user_id is None:
    #         print("User id is None. Cannot remove email account.")
    #         return 1
    
    #     # Get the email address from the user
    #     email = input("Please enter the email address you want to remove: ")
    #     # TODO - Check if the email is valid using third-party service?
    #     while not self.is_valid_email(email):
    #         print("Invalid email address, please try again. ", end="")
    #         email = input()

    #     # Sanitize the email address
    #     email = self.__sanitize_input(email)

    #     # Get the email_usage_id from the database
    #     email_usage_id = database.query_executor.get_email_usage_id(email_usage)

    #     # Check if the email address is already in the database
    #     if not database.query_executor.entry_exists("email",
    #             f"email_address='{email}' AND email_usage_id='{email_usage_id}'",
    #             self.session_manager.current_user.user_id):
    #         print("Email address already in database.")
    #         return 2

    #     # Add all the information to the database
    #     columns = ("email_address", "email_usage_id")
    #     values = (email, email_usage_id)
        
    #     # Insert the entry into the database
    #     database.delete_entry("email", columns, values, self.session_manager.current_user.user_id)
    #     print("Email account successfully removed.")
    #     return 0


    # def is_valid_email(self, email: str) -> bool:
    #     # Check if the email is valid
    #     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    #     return re.match(pattern, email) is not None

    

if __name__ == "__main__":
    pass
