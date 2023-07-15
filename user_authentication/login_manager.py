# Purpose: Login Manager module for managing the user interface for the login process and the login process itself.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication
from user_interface.user_input import UserInput

# Configure logging
import logging


# LoginManager class for managing the login process
class LoginManager:
    def __init__(self, session_manager: SessionManager, user_authentication: UserAuthentication) -> None:
        self.session_manager = session_manager
        self.user_authentication = user_authentication
        self.user_input = UserInput()
        logging.info("Login Manager initialized.")
    

    def create_account(self) -> None:
        print("Creating a new account...")

        # Get the username from the user
        provided_username = self.user_input.username_prompt()

        if provided_username is None:
            print("No username entered. Account creation failed. Please try again")
            return None
        
        # Check if the username already exists
        if self.user_authentication.query_executor.get_user_by_username(provided_username):
            print("Username already exists. Account creation failed. Please try again")
            return None

        # Get the password from the user
        provided_password = self.user_input.password_prompt(confirm=True)

        # Check if the password is valid
        if provided_password is None:
            print("No password entered. Account creation failed. Please try again")
            return None

        # Create the account
        self.user_authentication.query_executor.store_username_and_password(provided_username, provided_password)

        # Check if the account was created successfully
        user = self.user_authentication.query_executor.get_user_by_username(provided_username)
        if user:
            # Load the user into the session manager
            self.session_manager.current_user = user
            self.session_manager.logged_in = True
            self.session_manager.generate_session_token()
            self.session_manager.start_session()
            print("You are now logged in.")
            print("Account created successfully!")
            print("You are now logged in.")
            logging.debug(f"User created and logged in. User ID: {user.user_id}")
            # self.redirect_to_dashboard(session_token)
        else:
            print("Account creation failed. Please try again")
            logging.info(f"Account creation '{provided_username}' failed. No user ID.")


    def login(self) -> None:
        print("Logging in...")

        # Get the username from the user, sanitize it, and store it
        provided_username = self.user_input.username_prompt()

        # Check if the username exists
        user = self.user_authentication.query_executor.get_user_by_username(provided_username)
        if not user:
            print("Username does not exist. Account login failed. Please try again")
            return None
        else:
            print(f"Logging in as '{user.username}'...")

        # Get the password from the user
        provided_password_hash = self.user_input.password_prompt(confirm=False)

        # Verify the username and password
        if self.user_authentication.authenticate_user(provided_username, provided_password_hash):
            if self.session_manager.current_user is None:
                # Load the user into the session manager
                self.session_manager.current_user = user
                self.session_manager.logged_in = True
                print("You are now logged in.")
                logging.info(f"User '{user.username}' user_id '{user.user_id}' logged in with session token: {self.session_manager.session_token}")
            else:
                print("You are already logged in.")
                logging.info(f"User '{user.username}' user_id '{user.user_id}' is already logged in with session token: {self.session_manager.session_token}")
        else:
            print("Username or password is incorrect. Account login failed. Please try again")
            logging.info(f"User '{user.username}' user_id '{user.user_id}' failed to log in with session token: {self.session_manager.session_token}")


    def logout(self) -> None:
        print("Logging out...")
        username = None
        user_id = None
        session_token = self.session_manager.session_token
        if self.session_manager.current_user is None:
            print("No user is currently logged in.")
            logging.info(f"No user is currently logged in. Session token: {session_token}")
        else:
            username = self.session_manager.current_user.username
            user_id = self.session_manager.current_user.user_id
        self.session_manager.current_user = None
        self.session_manager.logged_in = False
        logging.info(f"User '{username}' user_id '{user_id}' logged out with session token: {session_token}")
        print("User logged out.")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
