# Purpose: Login Manager module for managing the login process.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules
from session.session_manager import SessionManager
from user_authentication.authentication import UserAuthentication

# Configure logging
import logging
from config import configure_logging
configure_logging()


# LoginManager class for managing the login process
class LoginManager:
    def __init__(self, session_manager: SessionManager, user_authentication: UserAuthentication) -> None:
        self.session_manager = session_manager
        self.user_authentication = user_authentication
        logging.info("Login Manager initialized.")


    def __sanitize_input(self, input: str) -> str:
        # Remove any potentially dangerous characters
        sanitized_input = input.translate(str.maketrans('', '', '\'"<>;'))
        return sanitized_input
    

    def __username_input(self, prompt: str = "Enter your username: ",) -> str:
        # Get the username from the user
        username = input(prompt)

        # Check if the username is valid
        while not re.match("^[a-zA-Z0-9_]*$", username):
            print("Invalid username. Only alphanumeric characters and underscores are allowed.")
            username = input("Please try again: ")

        # Sanitize the username
        username = self.__sanitize_input(username)

        return username


    def __password_input(self, prompt: str = "Enter your password: ", confirm: bool = False, confirm_prompt: str = "Confirm your password: ") -> bytes | None:
        # Get the password from the user
        password = getpass(prompt)

        # Confirm the password if confirm is True
        if confirm:
            confirm_password = getpass(confirm_prompt)

            # Check if the password and confirm_password match
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                return None
        
        # Convert the password to bytes
        password = password.encode()

        if confirm:
            # If confirm is True, hash the password (bytes) and return it as bytes
            return self.__hash_password(password)
        else:
            # If confirm is False, return the password as bytes
            return password


    def __hash_password(self, password: bytes) -> bytes:
        # Salt the password for extra security
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password


    def create_account(self) -> None:
        print("Creating a new account...")

        # Get the username from the user
        username = self.__username_input()

        if username is None:
            print("No username entered. Account creation failed. Please try again")
            return None
        
        # Check if the username already exists
        if self.user_authentication.query_executor.get_user_by_username(username):
            print("Username already exists. Account creation failed. Please try again")
            return None

        # Get the password from the user
        password = self.__password_input(confirm=True)

        # Check if the password is valid
        if password is None:
            print("No password entered. Account creation failed. Please try again")
            return None

        # Create the account
        self.user_authentication.query_executor.store_username_and_password(username, password)

        # Check if the account was created successfully
        user = self.user_authentication.query_executor.get_user_by_username(username)
        if user:
            self.session_manager.user_logging_in(user)
            print("Account created successfully!")
            print("You are now logged in.")
            logging.debug(f"User created and logged in. User ID: {user.user_id}")
            # self.redirect_to_dashboard(session_token)
        else:
            print("Account creation failed.")
            logging.debug(f"Account creation failed. No user ID.")
            return None


    def login(self) -> None:
        print("Logging in...")

        # Get the username from the user, sanitize it, and store it
        provided_username = self.__username_input()

        # Check if the username exists
        if provided_username is None:
            print("No username enterred. Account login failed. Please try again")
            return None

        # Check if the username exists
        user = self.user_authentication.query_executor.get_user_by_username(provided_username)
        if not user:
            print("Username does not exist. Account login failed. Please try again")
            return None
        else:
            print(f"Logging in as '{user.username}'...")

        # Get the password from the user
        provided_password_hash = self.__password_input()

        # Check if the password is valid
        if provided_password_hash is None:
            print("No password enterred. Account login failed. Please try again")
            return None

        # Verify the username and password
        if self.user_authentication.authenticate_user(provided_username, provided_password_hash):
            # Load the user into the session manager
            self.session_manager.user_logging_in(user)
            user = self.session_manager.current_user
            if user:
                print("You are now logged in.")
                logging.debug(f"User logged in. User ID: {user.user_id}")
                # session_token = self.user_authentication.generate_session_token(user_id)
                # self.redirect_to_dashboard(session_token)
            else:
                print("Account login failed.")
                logging.debug(f"Account login failed. No user ID.")
                return None


    def logout(self, session_token: str | None = None) -> None:
        print("Logging out...")
        self.session_manager.user_logging_out()
        if self.session_manager.current_user:
            print("User still logged in.")
            logging.debug(f"User still logged in. User ID: {self.session_manager.current_user.user_id}")
        else:
            print("User logged out.")
            # Perform additional logout actions
            # # Logout the user
            # self.user_authentication.logout_user(session_token)
            logging.info(f"User logged out with session token: {session_token}")


    # def redirect_to_dashboard(self, session_token):
    #     # Redirect the user to the dashboard page with the session token
    #     pass


if __name__ == "__main__":
    pass
