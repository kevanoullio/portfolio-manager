# Purpose: Authentication module for authenticating user and validating credentials of various types

# Standard Libraries
import secrets
import string

# Third-party Libraries
import bcrypt

# Local Modules
from session.session_manager import SessionManager
from user_interface.user_input import UserInput

# Configure logging
import logging


# Authentication class for authenticating user and validating credentials of various types
class Authentication:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager
        self.query_executor = self.session_manager.database.query_executor
        self.user_input = UserInput()
        logging.info("UserAuthentication initialized.")


    def authenticate_user(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Check if the provided credentials are valid
        if self.validate_user_credentials(provided_username, provided_password_hash):
            return True
        else:
            print("Account login failed. Please try again.")
            return False


    def validate_user_credentials(self, provided_username: str, provided_password_hash: bytes) -> bool:
        # Get a User class based on the username
        user = self.query_executor.get_user_by_username(provided_username)
        # Check if the user exists and the password matches
        if user and self.verify_password(provided_password_hash, user.password_hash):
            return True
        else:
            print("Invalid user credentials.")
            return False
    

    def validate_email_credentials(self, provided_email_address: str, provided_password_hash: bytes) -> bool | None:
        # Get an EmailAccount class based on the email
        email_account = self.query_executor.get_email_account_by_email_address(provided_email_address)
        # Check if the email account exists.
        if email_account:
            if email_account.password_hash is None:
            # If the email account was only added for notification purposes, the password hash will be None
                return None
            elif self.verify_password(provided_password_hash, email_account.password_hash):
                return True
        else:
            print("Invalid email credentials.")
            return False


    def verify_password(self, provided_password_hash: bytes, stored_password_hash: bytes) -> bool:
        # Verify if the provided password matches the user's stored password
        result = bcrypt.checkpw(provided_password_hash, stored_password_hash)
        return result


    def generate_session_token(self, length: int = 16) -> None:
        # Generates a random session token of the specified length
        characters = string.ascii_letters + string.digits
        session_token = ''.join(secrets.choice(characters) for _ in range(length))
        self.session_manager.session_token = session_token


    def verify_session_token(self, provided_session_token: str) -> bool:
        # TODO - utilize token verification for every transaction on the database
        # Get the session token from the database or cache
        current_session_token = self.session_manager.session_token
        # Check if the session token is present and matches the stored token
        if current_session_token and provided_session_token == current_session_token:
            # TODO - Add additional checks such as token expiration
            # Return True if the token is valid
            return True
        # Return False if the token is invalid or not present
        return False


    def clear_session_token(self) -> None:
        # Remove the session token from the database or cache
        self.session_manager.session_token = None



# To verify the session token, you typically perform the verification step at the beginning of each protected or restricted operation within your application. Here are some guidelines on when and where to verify the session token:

# 1. Authorization Middleware/Decorator: In many web frameworks, you can create middleware or decorators that intercept requests before they reach the protected routes or endpoints. Within this middleware or decorator, you can verify the session token. If the token is valid, the request is allowed to proceed to the corresponding route or endpoint. Otherwise, you can return an appropriate error response or redirect the user to the login page.

# 2. Protected Route/Endpoint: If you don't use middleware or decorators, you can directly verify the session token within the handler function of each protected route or endpoint. Perform the verification at the beginning of the function, and if the token is valid, allow the execution of the rest of the code. Otherwise, handle the unauthorized access appropriately.

# The session token used for verification should typically be obtained from the client's request. The token can be passed as a part of the request, usually in the form of an HTTP header, query parameter, or cookie. In your code, you can retrieve the session token from the request object provided by the web framework or from any other mechanism you use for session management.

# For example, in a Flask web application, you can retrieve the session token from the `request` object like this:

# ```python
# from flask import request

# class Authentication:
#     def verify_session_token(self):
#         session_token = request.headers.get('Authorization')
#         # Perform token verification logic here
# ```

# Remember to adapt the code based on the specific web framework or session management mechanism you are using.

# By verifying the session token at the appropriate entry points within your application, you ensure that only authenticated and authorized users can access protected functionality.

    

if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
