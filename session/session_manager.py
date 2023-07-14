# Purpose: Session Manager module for managing the current session state.

# Standard Libraries
import random
import secrets
import string

# Third-party Libraries

# Local Modules
from data_management.database import Database, DatabaseSnapshot
from user_authentication.user import User

# Configure logging
import logging


# SessionManager class for managing the current user session
class SessionManager:
    def __init__(self, database: Database) -> None:
        self.database: Database = database
        self.login_db_is_running: bool = False
        self.main_db_is_running: bool = False
        self.current_user: User | None = None
        self.logged_in: bool = False
        self.session_token = None
        self.modifications = []
        self.session_history = []
        logging.info("Session Manager initialized.")


    def generate_session_token(self, length: int = 16) -> None:
        # Generates a random session token of the specified length
        characters = string.ascii_letters + string.digits
        session_token = ''.join(secrets.choice(characters) for _ in range(length))
        self.session_token = session_token


    def start_session(self) -> None:
        # Generate a new session ID
        self.session_id = self.generate_session_token()
        # # Add the initial snapshot to session history
        # self.session_history.append(DatabaseSnapshot(self.database))
        # Clear the tracked modifications
        self.saved = False

        # Only keep the latest 100 snapshots
        if len(self.session_history) > 100:
            self.session_history.pop(0)  # Remove the oldest snapshot


    def track_modification(self, modification) -> None:
        # Track modifications made during the session
        if not self.saved:
            self.modifications.append(modification)


    def save_changes(self) -> None:
        # Apply the tracked modifications to the database
        if not self.saved:
            for modification in self.modifications:
                modification.execute()
            self.modifications = []
            self.saved = True
            print("Portfolio saved!")


    def discard_changes(self) -> None:
        # Clear the tracked modifications without applying them
        if not self.saved:
            self.modifications = []
            print("Most recent Portfolio changes discarded!")


    def rollback_changes(self) -> None:
        if len(self.session_history) > 1:
            # Remove the latest snapshot from session history
            self.session_history.pop()
            # Roll back the database to the previous snapshot
            previous_snapshot = self.session_history[-1]
            previous_snapshot.rollback()


    def close_session(self) -> None:
        if not self.saved and self.modifications:
            # Prompt the user to save or discard changes before exiting
            choice = input("Do you want to save changes? ([y]/n): ").strip().lower()
            if choice == "y" or choice == "":
                self.save_changes()
            elif choice == "n":
                self.discard_changes()
            else:
                while choice not in ["y", "n"]:
                    choice = input("Please enter a valid choice ([y]/n): ").strip().lower()
                if choice == "y":
                    self.save_changes()
                elif choice == "n":
                    self.discard_changes()

        # Clear session-related data
        self.session_token = None
        self.modifications = []
        self.session_history = []


    def exit_program(self) -> None:
        self.login_db_is_running = False
        logging.info("Login Dashboard has stopped running.")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
