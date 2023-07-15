# Purpose: Accounts module for defining all account types.

# Standard Libraries

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# User class for defining user account type
class User:
    def __init__(self, user_id: int, username: str, password_hash: bytes) -> None:
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        logging.info(f"User initialized successfully. Username: {self.username}, User ID: {self.user_id}")


    def update_username(self, new_username: str) -> None:
        # Update the user's username to the new username
        self.username = new_username


    def update_password(self, new_password_hash: bytes) -> None:
        # Update the user's password to the new password
        self.password_hash = new_password_hash


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






# EmailAccount class for defining email account type
class EmailAccount:
    def __init__(self, usage: str, address: str, password_hash: bytes | None = None) -> None:
        self.usage = usage
        self.address = address
        self.password_hash = password_hash



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
