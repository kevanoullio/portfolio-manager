# Purpose: User Account module for defining user account data type and its associated functionality.

# Standard Libraries
from dataclasses import dataclass

# Third-party Libraries

# Local Modules
from data_management.connection import DatabaseConnection

# Configure logging
import logging


# UserAccount class for defining user account data type
@dataclass
class UserAccount:
    user_id: int
    username: str
    password_hash: bytes

    def __post_init__(self) -> None:
        logging.info(f"User initialized successfully. Username: {self.username}, User ID: {self.user_id}")


class UserAccountService:
    def __init__(self, database_connection: DatabaseConnection):
        self.database_connection = database_connection

    def save_to_database(self, user_account: UserAccount) -> None:
        # Save the user's information to the database
        # Perform necessary database interactions to store user data
        pass

    def delete_from_database(self, user_account: UserAccount) -> None:
        # Delete the user's information from the database
        # Perform necessary database interactions to remove user data
        pass

    def get_user_account(self, user_id: int) -> UserAccount:
        # Logic to retrieve user account from the database based on user_id
        # TODO - Implement this method and fix return
        return UserAccount(user_id, "username", b"password_hash")

    def update_username(self, user_account: UserAccount, new_username: str) -> None:
        # Update the user's username to the new username
        user_account.username = new_username

    def update_password(self, user_account: UserAccount, new_password_hash: bytes) -> None:
        # Update the user's password to the new password
        user_account.password_hash = new_password_hash

    def deactivate_account(self, user_account: UserAccount) -> None:
        # Deactivate or disable the user's account
        # Perform any necessary cleanup or disable associated functionality
        pass

    def is_admin(self, user_account: UserAccount) -> bool:
        # Check if the user has admin privileges or roles
        # Return True if the user is an admin, False otherwise
        # TODO - Implement this method and fix return
        return False

    def get_profile(self, user_account: UserAccount) -> dict:
        # Retrieve and return the user's profile information
        # Return a dictionary containing profile data
        # TODO - Implement this method and fix return
        return {"username": user_account.username}


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
