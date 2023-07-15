# Purpose: Login Manager module for managing the user interface for the login process and the login process itself.

# Standard Libraries

# Third-party Libraries

# Local Modules
from account_management.accounts import User
from session.session_manager import SessionManager
from user_authentication.authentication import Authentication
from user_interface.user_input import UserInput

# Configure logging
import logging


# LoginManager class for managing the login process
class LoginManager:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.user_authentication = Authentication(self.session_manager)
        self.user_input = UserInput()
        logging.info("Login Manager initialized.")
    

    def create_account(self) -> None:
        print("Creating a new account...")

        # Get the username from the user (username_prompt checks if it's valid)
        provided_username = self.user_input.username_prompt()
        
        # Check if the username already exists
        if self.session_manager.database.query_executor.get_user_by_username(provided_username):
            print("Username already exists. Account creation failed. Please try again")
            return None

        # Get the password from the user (password_prompt checks if it's valid), confirm it with a second prompt
        provided_password = self.user_input.password_prompt(confirm=True)

        # Create the account
        self.session_manager.database.query_executor.store_username_and_password(provided_username, provided_password)

        # Check if the account was created successfully
        user = self.session_manager.database.query_executor.get_user_by_username(provided_username)
        if user:
            # Run the login_management function to log the user in
            self.login_management(user)
            # Print the success message
            self.account_creation_success_message(user.username)
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
        user = self.session_manager.database.query_executor.get_user_by_username(provided_username)
        if not user:
            print("Username does not exist. Account login failed. Please try again")
            return None
        else:
            print(f"Logging in as '{user.username}'...")

        # Get the password from the user (password_prompt checks if it's valid)
        provided_password_hash = self.user_input.password_prompt()

        # Verify the username and password
        if self.user_authentication.authenticate_user(provided_username, provided_password_hash):
            if self.session_manager.current_user is None:
                # Run the login_management function to log the user in
                self.login_management(user)
                # Print the success message
                self.login_success_message(user.username)
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
        # Run the logout_management function to log the user out
        self.logout_management()
        # Print the success message
        self.logout_success_message(f"{username}")
        logging.info(f"User '{username}' user_id '{user_id}' logged out with session token: {session_token}")
        print("User logged out.")


    def login_management(self, user: User) -> None:
        # Load the user into the session manager
        self.session_manager.current_user = user
        self.session_manager.logged_in = True
        # Generate a session token and start the session
        self.user_authentication.generate_session_token()
        self.session_manager.start_session()

    
    def logout_management(self) -> None:
        # Unload the user from the session manager
        self.session_manager.current_user = None
        self.session_manager.logged_in = False
        # Clear the session token and close the session
        self.user_authentication.clear_session_token()
        self.session_manager.close_session()


    def account_creation_success_message(self, username: str) -> None:
        print("Account creation successful!")
        print(f"You are now logged in as '{username}'")


    def login_success_message(self, username: str) -> None:
        print("Login successful!")
        print(f"You are now logged in as '{username}'")
    

    def logout_success_message(self, username: str) -> None:
        print("Logout successful!")
        print(f"User '{username}' is now logged out.")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
