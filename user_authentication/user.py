# Purpose: User module for managing user-related functionality.

# Standard Libraries

# Third-party Libraries
import bcrypt

# Local Modules

# Configure logging
import logging


# EmailAccount class for managing email account-related functionality
class EmailAccount:
    def __init__(self, type: str, email_address: str, password_hash: bytes | None = None) -> None:
        self.type = type
        self.address = email_address
        self.password_hash = password_hash


    def verify_password(self, provided_password_hash: bytes) -> bool | None:
        if self.password_hash is None:
            # If the email account was only added for notification purposes, the password hash will be None
            return None
        else:
            # Verify if the provided password matches the email account's stored password
            result = bcrypt.checkpw(provided_password_hash, self.password_hash)
            return result
    

    def import_data(self):
        # Logic to import data from the email account
        pass

    def send_notification(self):
        # Logic to send a notification to the email account
        pass


# User class for managing user-related functionality
class User:
    def __init__(self, user_id: int, username: str, password_hash: bytes, email_accounts: list[EmailAccount] | None = None) -> None:
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email_accounts = email_accounts or []
        logging.info(f"User initialized successfully. Username: {self.username}, User ID: {self.user_id}")


    def update_username(self, new_username: str) -> None:
        # Update the user's username to the new username
        self.username = new_username


    def verify_user_password(self, provided_password_hash: bytes) -> bool:
        # Verify if the provided password matches the user's stored password
        result = bcrypt.checkpw(provided_password_hash, self.password_hash)
        return result


    def update_user_password(self, new_password_hash: bytes) -> None:
        # Update the user's password to the new password
        self.password_hash = new_password_hash


    def get_email_account(self, email_address: str) -> EmailAccount | None:
        # Get the email account from the user's email accounts
        for email_account in self.email_accounts:
            if email_account.address == email_address:
                return email_account
            else:
                print("Email account not found.")
                return None


    def verify_email_password(self, email_address: str, provided_password_hash: bytes) -> bool | None:
        # Get the email account from the user's email accounts
        email_account = self.get_email_account(email_address)
        # Verify if the provided password matches the email account's stored password
        if email_account:
            result = email_account.verify_password(provided_password_hash)
            return result
        else:
            return False


    def add_email_account(self, email_account) -> None:
        self.email_accounts.append(email_account)


    def remove_email_account(self, email_account) -> None:
        self.email_accounts.remove(email_account)



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
    print("This module is not meant to be executed directly.")
