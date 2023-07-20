# Purpose: Authentication module for authenticating user and validating credentials of various types.

# Standard Libraries

# Third-party Libraries
import bcrypt

# Local Modules
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from database_management.database import Database

# Configure logging
import logging


# Authentication class for authenticating user and validating credentials of various types
class AccountAuthenticator:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.user_account_operation = UserAccountOperation(self.database)
        self.email_account_operation = EmailAccountOperation(self.database)
        logging.debug("UserAuthentication initialized.")

    def validate_user_credentials(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Get the user account password hash
        user_account_password_hash: bytes | None = self.user_account_operation.get_user_password_by_username(provided_username)
        # Check if the provided password and the stored user account password match
        if user_account_password_hash is None:
            print("Username is in the database, but doesn't have an associated password.")
            return False
        else:
            if self.verify_password(provided_password_hash, user_account_password_hash):
                print("User authenticated.")
                return True
            else:
                print("Invalid user credentials.")
                return False

    def validate_email_credentials(self, provided_email_address: str, provided_password_hash: bytes) -> bool | None:
        # TODO - put the commented out code in EmailAccountOperation
        # # Get an EmailAccount class based on the email
        # email_account: EmailAccount | None = self.email_account_operation.get_email_account_by_email_address(provided_email_address)
        # # Check if the email account exists.
        # if email_account is None:
        #     print("Email address is not in the database.")
        #     return None
        # Get the email account password hash
        email_account_password_hash: bytes | None = self.email_account_operation.get_email_password_by_email_address(provided_email_address)
        # Check if the email password exists.
        if email_account_password_hash is None:
            # If the email account was only added for notification purposes, the password hash will be None
            print("Email address is in the database, but doesn't have an associated password.")
            return None
        else:
            if self.verify_password(provided_password_hash, email_account_password_hash):
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
