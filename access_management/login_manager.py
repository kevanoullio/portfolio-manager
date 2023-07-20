# Purpose: Login Manager module for managing the user interface for the login process and the login process itself.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from session_management.session_manager import SessionManager
from database_management.database import Database
from account_management.account_operations import UserAccountOperation
from access_management.account_authenticator import AccountAuthenticator
from session_management.token_manager  import SessionTokenManager
from user_interface.user_input import UserInput

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging

# from data_management.query.query_builder import QueryBuilder
# class LoginManager:
#     def __init__(self, database):
#         self.database = database

#     def validate_user(self, username, password):
#         # Construct a SELECT statement using the QueryBuilder
#         query = QueryBuilder('users').select(['id', 'name', 'email']).where('username', '=', username).where('password', '=', password).build()

#         # Execute the query using the database object
#         result = self.database.execute_query(query)

#         # Check if the user credentials are valid
#         is_valid = result.fetchone() is not None

#         return is_valid

#     def validate_user(self, username, password):
#         # Use the with_connection method to manage the database connection
#         is_valid = self.database.with_connection(lambda connection: self.validate_user_with_connection(username, password, connection))

#         return is_valid

#     def validate_user_with_connection(self, username, password, connection):
#         # Construct a SELECT statement using the QueryBuilder
#         query = QueryBuilder('users').select(['id', 'name', 'email']).where('username', '=', username).where('password', '=', password).build()

#         # Execute the query using the provided connection object
#         cursor = connection.execute(query)
#         result = cursor.fetchone()

#         # Check if the user credentials are valid
#         is_valid = result is not None

#         return is_valid



# LoginManager class for managing the login process
class LoginManager:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.session_manager = self.database.session_manager
        self.session_token_manager = SessionTokenManager(self.session_manager)
        self.account_authenticator = AccountAuthenticator(self.database)
        self.user_input = UserInput()
        logging.info("Login Manager initialized.")

    def check_username_exists(self, provided_username: str) -> UserAccount | None:
        # FIXME - need to fix query_executor connection
        return self.database.query_executor.get_user_account_by_username(provided_username)

    def get_password(self):
        return self.user_input.password_prompt()

    def authenticate_user(self, provided_username, provided_password_hash):
        return self.account_authenticator.validate_user_credentials(provided_username, provided_password_hash)

    def create_account(self) -> None:
        # Get the username from the user (username_prompt checks if it's valid)
        provided_username = self.user_input.username_prompt()
        
        # Check if the username already exists
        if self.check_username_exists(provided_username):
            print("Username already exists. Account creation failed. Please try again")
            return None

        # Get the password from the user (password_prompt checks if it's valid), confirm it with a second prompt
        provided_password = self.user_input.password_prompt(confirm=True)

        # Create the account
        self.database.query_executor.store_username_and_password(provided_username, provided_password)

        # Check if the account was created successfully
        user_account = self.check_username_exists(provided_username)
        if user_account is not None:
            # Run the login_management function to log the user in
            self.execute_login_operations(user_account)
            # Print the success message
            print("Account creation success!")
            print(f"You are now logged in as '{user_account.username}'")
            logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' created and logged in with session token: {self.session_manager.get_session_token()}")
            # self.redirect_to_dashboard(session_token)
        else:
            print("Account creation failed. Please try again")
            logging.info(f"Account creation '{provided_username}' failed. No user ID.")

    def login(self) -> None:
        # Get the username from the user, sanitize it, and store it
        provided_username = self.user_input.username_prompt()

        # Check if the username exists
        user_account = self.check_username_exists(provided_username)
        if user_account is None:
            print("Username does not exist. Account login failed. Please try again")
            return None
        else:
            print(f"Logging in as '{user_account.username}'...")

        # Get the password from the user (password_prompt checks if it's valid)
        provided_password_hash = self.get_password()

        # Verify the username and password
        if self.authenticate_user(provided_username, provided_password_hash):
            if self.session_manager.get_current_user() is None:
                # Run the login_management function to log the user in
                self.execute_login_operations(user_account)
                # Print the success message
                print("Login success!")
                print(f"You are now logged in as '{user_account.username}'")
                logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' logged in with session token: {self.session_manager.get_session_token()}")
            else:
                print("You are already logged in.")
                logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' is already logged in with session token: {self.session_manager.get_session_token()}")
        else:
            print("Account login failed. Please try again")
            logging.info(f"User '{user_account.username}' user_id '{user_account.user_id}' failed to log in with session token: {self.session_manager.get_session_token()}")

    def logout(self) -> None:
        current_user = self.session_manager.get_current_user()
        session_token = self.session_manager.get_session_token()
        user_id = None
        username = None
        if current_user is None:
            print("No user is currently logged in.")
            logging.info(f"No user is currently logged in. Session token: {session_token}")
        else:
            username = current_user.username
            user_id = current_user.user_id
        # Run the logout_management function to log the user out
        self.execute_logout_operations()
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

    def execute_login_operations(self, user: UserAccount) -> None:
        # Load the user into the session manager
        self.session_manager.set_current_user(user)
        # Generate a session token and start the session
        self.session_token_manager.generate_session_token()
        self.session_manager.start_session()
    
    def execute_logout_operations(self) -> None:
        # Unload the user from the session manager
        self.session_manager.set_current_user(None)
        # Clear the session token and close the session
        self.session_token_manager.clear_session_token()
        self.session_manager.close_session()


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
