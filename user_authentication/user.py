# Purpose: User module for managing user-related functionality.

# Standard Libraries

# Third-party Libraries
import bcrypt

# Local Modules

# Configure logging
import logging
from config import configure_logging
configure_logging()

# Start using logging
logging.debug("This is a debug message.")


# EmailAccount class for managing email account-related functionality
class EmailAccount:
    def __init__(self, email_type: str, email_address: str, password_hash: bytes | None = None) -> None:
        self.email_type = email_type
        self.email_address = email_address
        self.password_hash = password_hash

    def import_data(self):
        # Logic to import data from the email account
        pass

    def send_notification(self, message):
        # Logic to send a notification to the email account
        pass


# User class for managing user-related functionality
class User:
    def __init__(self, user_id: int, username: str, password_hash: bytes, email_accounts: list[EmailAccount] | None = None) -> None:
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email_accounts = email_accounts or []


    def verify_password(self, provided_password_hash: bytes) -> bool:
        # Verify if the provided password matches the user's stored password
        result = bcrypt.checkpw(provided_password_hash, self.password_hash)
        return result


    def update_password(self, new_password_hash: bytes) -> None:
        # Update the user's password to the new password
        self.password_hash = new_password_hash


    def add_email_account(self, account_type: str, email_address: str, password_hash: bytes | None = None) -> None:
        email_account = EmailAccount(account_type, email_address, password_hash)
        self.email_accounts.append(email_account)


    def remove_email_account(self, email_address: str) -> None:
        self.email_accounts = [account for account in self.email_accounts if account.email_address != email_address]


    # def deactivate_account(self) -> None:
    #     # Deactivate or disable the user's account
    #     # Perform any necessary cleanup or disable associated functionality
    #     pass


    # def is_admin(self) -> bool:
    #     # Check if the user has admin privileges or roles
    #     # Return True if the user is an admin, False otherwise
    #     pass


    # def get_profile(self) -> dict:
    #     # Retrieve and return the user's profile information
    #     # Return a dictionary containing profile data
    #     pass


    # def save_to_database(self) -> None:
    #     # Save the user's information to the database
    #     # Perform necessary database interactions to store user data
    #     pass


    # def delete_from_database(self) -> None:
    #     # Delete the user's information from the database
    #     # Perform necessary database interactions to remove user data
    #     pass

    # Additional methods for user-related functionality


if __name__ == "__main__":
    pass
