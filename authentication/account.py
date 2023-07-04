# Purpose: Account class for user authentication and account management.

# Standard Libraries
from getpass import getpass

# Third-party Libraries
import bcrypt

# Local Modules
from database.database import Database


# Class Definitions
class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = self._hash_password(password)
        self.logged_in = False


    def login(self):
        if not self.logged_in:
            print(f"Logging in as {self.username}...")
            # Code for logging into the account
            # Example: Use a third-party library or API to authenticate the user
            self.logged_in = True
            print("Login successful.")
        else:
            print("You are already logged in.")


    def logout(self):
        if self.logged_in:
            print("Logging out...")
            # Code for logging out of the email account
            # Example: Use a third-party library or API to log out
            self.logged_in = False
            print("Logout successful.")
        else:
            print("You are not logged in.")


    def create_account(self, database: Database):
        print("Creating a new account...")
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        confirm_password = getpass("Confirm your password: ")

        if password != confirm_password:
            print("Passwords do not match. Account creation failed.")
            return

        self.username = username
        self.password = self._hash_password(password)
        database.store_username_and_password(self.username, self.password)
        print("Account creation successful.")


    def _hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password


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
        self.logged_in = False


if __name__ == "__main__":
    database = Database("db_file_test.db")
    
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    account = Account(username, password)

    account.create_account(database)
    account.login()
    account.modify_account()
    account.delete_account()
