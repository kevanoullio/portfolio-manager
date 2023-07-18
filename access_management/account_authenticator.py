# Purpose: Authentication module for authenticating user and validating credentials of various types

# Standard Libraries
import secrets
import string

# Third-party Libraries
import bcrypt

# Local Modules
from account_management.accounts import EmailAccount, UserAccount

# Configure logging
import logging


# Authentication class for authenticating user and validating credentials of various types
class AccountAuthenticator:
    def __init__(self) -> None:
        logging.info("UserAuthentication initialized.")


    def set_session_manager(self, session_manager):
        self.session_manager = session_manager


    def authenticate_user(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Check if the provided credentials are valid
        if self.validate_user_credentials(provided_username, provided_password_hash):
            return True
        else:
            print("Account login failed. Please try again.")
            return False


    def validate_user_credentials(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Get a User class based on the username
        user: UserAccount | None = self.session_manager.database.query_executor.get_user_by_username(provided_username)
        # Check if the user exists and the password matches
        if user and self.verify_password(provided_password_hash, user.password_hash):
            return True
        else:
            print("Invalid user credentials.")
            return False
    

    def validate_email_credentials(self, provided_email_address: str, provided_password_hash: bytes) -> bool | None:
        # Get an EmailAccount class based on the email
        email_account: EmailAccount | None = self.session_manager.database.query_executor.get_email_account_by_email_address(provided_email_address)
        # Check if the email account exists.
        if email_account:
            if email_account.password_hash is None:
            # If the email account was only added for notification purposes, the password hash will be None
                return None
            elif self.verify_password(provided_password_hash, email_account.password_hash):
                return True
        else:
            print("Invalid email credentials.")
            return False


    def verify_password(self, provided_password_hash: bytes, stored_password_hash: bytes) -> bool:
        # Verify if the provided password matches the user's stored password
        result = bcrypt.checkpw(provided_password_hash, stored_password_hash)
        return result

    

if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
