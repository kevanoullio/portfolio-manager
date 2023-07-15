# Purpose: Authentication module for authenticating users and managing user accounts.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules
from session.session_manager import SessionManager
from user_authentication.user import EmailAccount, User
from user_interface.user_input import UserInput

# Configure logging
import logging


# UserAuthentication class for managing user authentication
class UserAuthentication:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.query_executor = self.session_manager.database.query_executor
        self.user_input = UserInput()
        logging.info("UserAuthentication initialized.")


    def authenticate_user(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Check if the provided credentials are valid
        if self.validate_user_credentials(provided_username, provided_password_hash):
            # Perform additional checks or actions if needed
            print("Login successful!")
            return True
        else:
            print("Account login failed. Please try again.")
            return False


    def validate_user_credentials(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Get a User class based on the username
        user = self.query_executor.get_user_by_username(provided_username)
        # Check if the user exists and the password matches
        if user and user.verify_user_password(provided_password_hash):
            return True
        else:
            print("Invalid user credentials.")
            return False
    

    def validate_email_credentials(self, provided_email: str, provided_password_hash: bytes) -> bool:
        # Check if the user exists
        if self.session_manager.current_user is None:
            print("No user is logged in.")
            return False
        # Check if the email account exists
        email_account = self.session_manager.current_user.get_email_account(provided_email)
        if email_account and email_account.verify_password(provided_password_hash):
            return True
        else:
            print("Invalid email credentials.")
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



    def import_email_account(self, email_usage: str) -> int:
        if self.session_manager.current_user is None:
            print("You are not logged in.")
            return 1

        # Get the email address from the user (email_prompt checks if it's valid)
        provided_email = self.user_input.email_prompt()

        # Get the email_usage_id from the database
        email_usage_id = self.query_executor.get_email_usage_id(email_usage)

        # Check if the email address is already in the database
        if self.query_executor.entry_exists("email",
                f"email_address='{provided_email}' AND email_usage_id='{email_usage_id}'",
                self.session_manager.current_user.user_id):
            print("Email address already in the database.")
            return 2
        
        # Only get the email password if the email usage is not "notification"
        if email_usage is "notification":
            provided_password = None
            # Prep the email information for insertion into the database
            columns = ("email_address", "email_usage_id")
            values = (provided_email, email_usage_id)
        else:
            # Get the password from the user (password_prompt checks if it's valid)
            provided_password = self.user_input.password_prompt(prompt="Enter your email password", confirm=True)
            # Prep the email information for insertion into the database
            columns = ("email_address", "password_hash", "email_usage_id")
            values = (provided_email, provided_password, email_usage_id)
        
        # Insert the entry into the database
        try:
            self.query_executor.insert_entry("email", columns, values, self.session_manager.current_user.user_id)
            # Add the email account to the current user
            self.session_manager.current_user.add_email_account(EmailAccount(email_usage, provided_email, provided_password))
        except Exception as e:
            print("Error inserting email account into the database.")
            logging.warning(e)
            return 3

        print("Email account import successful.")
        return 0


    def remove_email_account(self, email_usage: str) -> int:
        if self.session_manager.current_user is None:
            print("You are not logged in.")
            return 1
        # if self.session_manager.current_user.user_id is None:
        #     print("User id is None. Cannot remove email account.")
        #     return 1
    
        # Get the email address from the user (email_prompt checks if it's valid)
        provided_email = self.user_input.email_prompt()

        # Get the email_usage_id from the database
        email_usage_id = self.query_executor.get_email_usage_id(email_usage)

        # Check that the email address is in the database
        if not self.query_executor.entry_exists("email",
                f"email_address='{provided_email}' AND email_usage_id='{email_usage_id}'",
                self.session_manager.current_user.user_id):
            print("Email address is not in the database.")
            return 2

        # Only get the email password if the email usage is not "notification"
        if email_usage is "notification":
            provided_password = None
            # Prep the email information for insertion into the database
            columns = ("email_address", "email_usage_id")
            values = (provided_email, email_usage_id)
        else:
            # Get the password from the user (password_prompt checks if it's valid)
            provided_password = self.user_input.password_prompt(prompt="Enter your email password", confirm=True)
            # Verify the email password
            if not self.validate_email_credentials(provided_email, provided_password):
                print("Invalid email credentials.")
                return 2
            # Prep the email information for insertion into the database
            columns = ("email_address", "password_hash", "email_usage_id")
            values = (provided_email, provided_password, email_usage_id)
        
        # Delete the entry from the database
        try:
            self.query_executor.delete_entry("email", columns, values, self.session_manager.current_user.user_id)
            # Remove the email account from the current user
            self.session_manager.current_user.remove_email_account(EmailAccount(email_usage, provided_email, provided_password))
        except Exception as e:
            print("Error deleting email account from the database.")
            logging.warning(e)
            return 3
        
        print("Email account successfully removed.")
        return 0
    

if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
