# Purpose: Login Manager module for managing the user interface for the login process and the login process itself.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.database import Database
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from access_management.account_authenticator import AccountAuthenticator
from session_management.token_manager  import SessionTokenManager
from user_interface.user_input import UserInput

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# LoginManager class for managing the login process
class LoginManager:
    def __init__(self, database: Database) -> None:
        self._database = database
        self._session_token_manager = SessionTokenManager(self._database._session_manager)
        # TODO - may nee to pass account operation as arguments since they'll be used elsewhere
        self.user_account_operation = UserAccountOperation(self._database)
        self.email_account_operation = EmailAccountOperation(self._database)
        self._account_authenticator = AccountAuthenticator(self.user_account_operation, self.email_account_operation)
        self.user_input = UserInput()
        logging.debug("Login Manager initialized.")

    def create_account(self) -> None:
        # Get the username from the user (username_prompt checks if it's valid)
        provided_username = self.user_input.username_prompt()
        
        # Check if the username already exists
        if self.user_account_operation.check_username_exists(provided_username):
            print("Username already exists. Account creation failed. Please try again")
            return None

        # Get the password from the user (password_prompt checks if it's valid), confirm it with a second prompt
        provided_password = self.user_input.password_prompt(confirm=True)

        # Create the account
        self.user_account_operation.create_user_account(provided_username, provided_password)

        # Retrieve the created user account, will return None if creation failed
        user_account = self.user_account_operation.get_user_account_by_username(provided_username)
        if user_account is not None:
            # Run the login_management function to log the user in
            self._execute_login_operations(user_account)
            # Print the success message
            print("Account creation success!")
            print(f"You are now logged in as '{user_account.username}'")
            logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' created and logged in with session token: {self._database._session_manager.get_session_token()}")
            # self.redirect_to_dashboard(session_token)
        else:
            print("Account creation failed. Please try again.")
            logging.info(f"Account creation '{provided_username}' failed. No user ID.")

    def user_login(self) -> None:
        # Get the username from the user, sanitize it, and store it
        provided_username = self.user_input.username_prompt()

        # Check if the username exists, will return None if it doesn't
        user_account = self.user_account_operation.get_user_account_by_username(provided_username)
        if user_account is None:
            print("Username does not exist. Account login failed. Please try again.")
            return None
        else:
            print(f"Logging in as '{user_account.username}'...")

        # Get the password from the user (password_prompt checks if it's valid)
        provided_password_hash = self.user_input.password_prompt()

        # Verify the username and password
        if self._account_authenticator.validate_user_credentials(provided_username, provided_password_hash):
            if self._database._session_manager.get_current_user() is None:
                # Run the login_management function to log the user in
                self._execute_login_operations(user_account)
                # Print the success message
                print("Login success!")
                print(f"You are now logged in as '{user_account.username}'")
                logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' logged in with session token: {self._database._session_manager.get_session_token()}")
            else:
                print("You are already logged in.")
                logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' is already logged in with session token: {self._database._session_manager.get_session_token()}")
        else:
            print("Account login failed. Please try again")
            logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' failed to log in with session token: {self._database._session_manager.get_session_token()}")

    def user_logout(self) -> None:
        current_user = self._database._session_manager.get_current_user()
        session_token = self._database._session_manager.get_session_token()
        user_id = None
        username = None
        if current_user is None:
            print("No user is currently logged in.")
            logging.info(f"No user is currently logged in. Session token: {session_token}")
        else:
            username = current_user.username
            user_id = current_user.user_id
        # Run the logout_management function to log the user out
        self._execute_logout_operations()
        # Check that the logout was successful
        if current_user is not None:
            print("User logout failed!")
            print(f"User '{username}' is still logged in.")
            logging.info(f"User '{username}' not logged out.")
        else:
            # Print the success message
            print("Logout success!")
            print(f"User '{username}' is now logged out.")
            logging.info(f"User '{username}' user_id '{user_id}' logged out with session token: {session_token}")

    def _execute_login_operations(self, user: UserAccount) -> None:
        # Load the user into the session manager
        self._database._session_manager.set_current_user(user)
        # Generate a session token and start the session
        self._session_token_manager.generate_session_token()
        self._database._session_manager.start_session()
    
    def _execute_logout_operations(self) -> None:
        # Unload the user from the session manager
        self._database._session_manager.set_current_user(None)
        # Clear the session token and close the session
        self._session_token_manager.clear_session_token()
        self._database._session_manager.close_session()


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
