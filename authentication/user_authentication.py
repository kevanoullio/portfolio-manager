# Purpose: Account class for user authentication and account management.

# Standard Libraries
from getpass import getpass
import re

# Third-party Libraries
import bcrypt

# Local Modules
from database.database import Database


# UserAuthentication class
class UserAuthentication:
    def __init__(self, database: Database) -> None:
        self.database: Database = database
        self.logged_in: bool = False
        self.__username: str | None = None
        self.__password: bytes | None = None
        self.__current_user_id: int | None = None


    def get_username(self) -> str | None:
        if self.__username is not None:
            return self.__username
        else:
            return None

    def get_password(self) -> bytes | None:
        if self.__password is not None:
            return self.__password
        else:
            return None
    
    def get_current_user_id(self) -> int | None:
        return self.__current_user_id
    
    def set_username(self, username: str) -> None:
        self.__username = username

    def set_password(self, password: bytes, hash: bool = False) -> None:
        if hash:
            self.__password = self.__hash_password(password)
        else:
            self.__password = password
    
    def set_current_user_id(self, user_id: int) -> None:
        self.__current_user_id = user_id


    def __sanitize_input(self, input: str) -> str:
        # Remove any potentially dangerous characters
        sanitized_input = input.translate(str.maketrans('', '', '\'"<>;'))
        return sanitized_input
    

    def __username_input(self) -> None:
        # Get the username from the user
        username = input("Enter your username: ")

        # Check if the username is valid
        while not re.match("^[a-zA-Z0-9_]*$", username):
            print("Invalid username. Only alphanumeric characters and underscores are allowed.")
            username = input("Please try again: ")

        # Sanitize the username
        username = self.__sanitize_input(username)

        # Set the username
        self.set_username(username)


    def __password_input(self, prompt: str = "Enter your password: ", confirm: bool = False, confirm_prompt: str = "Confirm your password: ") -> None:
        # Get the password from the user
        password = getpass(prompt)

        # Confirm the password if confirm is True
        if confirm:
            confirm_password = getpass(confirm_prompt)

            # Check if the password and confirm_password match
            while password != confirm_password:
                print("Passwords do not match.")
                password = getpass("Please try again: ")
        
        # Convert the password to bytes
        password = password.encode()

        # Set the password
        if confirm:
            self.set_password(password, hash=True)
        else:
            self.set_password(password)


    def __hash_password(self, password: bytes) -> bytes:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        return hashed_password


    def create_account(self) -> int:
        print("Creating a new account...")
        
        # Get the username from the user
        self.__username_input()
        username = self.get_username()

        if username is None:
            print("Account creation failed.")
            return 1

        # Check if the username already exists
        if self.database.username_exists(username):
            print("Username already exists. Account creation failed.")
            return 1

        # Get the password from the user
        self.__password_input(confirm=True)
        password = self.get_password()

        if password is None:
            print("Account creation failed.")
            return 1

        # Create the account
        self.database.store_username_and_password(username, password)
        print("Account creation successful.")
        
        # Load the user id of the created account
        self.__load_user_id(username)

        # Log the user in
        self.logged_in = True
        print("Login successful.")
        return 0


    def login(self) -> int:
        if self.logged_in:
            print("You are already logged in.")
            return 0
        
        print("Logging in...")

        # Get the username from the user
        self.__username_input()
        username = self.get_username()

        if username is None:
            print("Account login failed.")
            return 1

        # Check if the username exists
        if not self.database.username_exists(username):
            print("Account login failed. Username does not exist.")
            return 1
        
        # Get the password from the user
        self.__password_input()
        password = self.get_password()

        if password is None:
            print("Account login failed. Password is None.")
            return 1

        # Retrieve the hashed password from the database
        stored_password_hash = self.database.get_password_hash(username)

        # Verify the entered password
        if bcrypt.checkpw(password, stored_password_hash):
            print(f"Logging in as {username}...")
            # Load the user id of the current account
            self.__load_user_id(username)
            self.logged_in = True
            print("Login successful.")
            return 0
        else:
            print("Password is incorrect. Account login failed.")
            return 1

    
    def logout(self) -> int:
        if self.logged_in:
            # Log the user out
            print("Logging out...")
            # Unload the user id of the current account
            self.__unload_user_id()
            self.logged_in = False
            print("Logout successful.")
            return 0
        else:
            print("You are not logged in.")
            return 1


    def modify_account(self):
        print("Modifying the account...")
        # Code for modifying the account
        # Example: Use a third-party library or API to modify the account
        print("Account modification successful.")


    def delete_account(self):
        print("Deleting the account...")
        # Code for deleting the account
        # Example: Use a third-party library or API to delete the account
        print("Account deletion successful.")
        # Unload the user id of the deleted account
        self.__unload_user_id()
        self.logged_in = False


    def import_email_account(self, database: Database) -> int:
        if self.current_user_id is None:
            print("You are not logged in.")
            return 1

        # Get the email address from the user
        email = input("Please enter the email address: ")
        # TODO - Check if the email address is valid, use third-party service?
        if not self.is_valid_email(email):
            print("Invalid email address, please try again. ", end="")

        # Sanitize the email address
        email = self.__sanitize_input(email)

        # Check if the email address is already in the database
        if database.check_entry_exists("email",
                f"email_address='{email}' AND email_usage_id='import_email_account'",
                self.current_user_id):
            print("Email address already in database.")
            return 0
        
        # Get the password from the user
        self.__password_input("Please enter the email password: ")
        password = self.get_password()

        if password is None:
            print("Account login failed. Password is None.")
            return 1

        # Add all the information to the database
        columns = ["email_address", "password_hash", "email_usage_id"]
        values = [email, password, "import_email_account"]
        
        # Insert the entry into the database
        database.insert_entry(self.current_user_id, "email", columns, values)
        print("Email account import successful.")
        return 0


    def is_valid_email(self, email: str) -> bool:
        # Check if the email is valid
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    
    def __load_user_id(self, username: str) -> None:
        self.current_user_id = self.database.get_user_id(username)

    
    def __unload_user_id(self) -> None:
        self.current_user_id = None

    

if __name__ == "__main__":
    database = Database("db_file_test.db")

    user_auth = UserAuthentication(database)

    user_auth.create_account()
    user_auth.login()
    user_auth.modify_account()
    user_auth.delete_account()




# 1. Secure Application Design:
#    - Implement secure coding practices to protect against common vulnerabilities like SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF).
#    - Use parameterized queries or ORM (Object-Relational Mapping) frameworks to prevent SQL injection attacks.
#    - Sanitize and validate user input to prevent malicious code execution.
#    - Implement secure session management techniques, such as using session tokens, secure cookies, or JWT (JSON Web Tokens).
