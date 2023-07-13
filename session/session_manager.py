# Purpose: Session Manager module for managing the current session state.

# Standard Libraries
import random
import string

# Third-party Libraries

# Local Modules
from data_management.database import Database, DatabaseSnapshot
from user_authentication.user import User

# Configure logging
import logging
from config import configure_logging
configure_logging()


# SessionManager class for managing the current user session
class SessionManager:
    def __init__(self, database: Database) -> None:
        self.database = database
        self.login_db_is_running: bool = False
        self.main_db_is_running: bool = False
        self.current_user: User | None = None
        self.logged_in: bool = False
        self.session_id = None
        self.modifications = []
        self.session_history = []
        logging.info("Session Manager has been initialized.")
    

    def user_logging_in(self, current_user: User) -> None:
        self.current_user = current_user
        self.logged_in = True


    def user_logging_out(self) -> None:
        self.current_user = None
        self.logged_in = False


    def generate_session_id(self, length:int = 10) -> str:
        # Generate a random session ID consisting of alphanumeric characters
        characters = string.ascii_letters + string.digits
        session_id = ''.join(random.choices(characters, k=length))
        return session_id


    def start_session(self) -> None:
        # Generate a new session ID
        self.session_id = self.generate_session_id()
        # Add the initial snapshot to session history
        self.session_history.append(DatabaseSnapshot(self.database))


    def track_modification(self, modification) -> None:
        # Track modifications made during the session
        self.modifications.append(modification)


    def save_changes(self) -> None:
        # Apply the tracked modifications to the database
        for modification in self.modifications:
            modification.execute()
        self.modifications = []


    def discard_changes(self) -> None:
        # Clear the tracked modifications without applying them
        self.modifications = []


    def rollback_changes(self) -> None:
        if len(self.session_history) > 1:
            # Remove the latest snapshot from session history
            self.session_history.pop()
            # Roll back the database to the previous snapshot
            previous_snapshot = self.session_history[-1]
            previous_snapshot.rollback()


    def exit_session(self) -> None:
        if self.modifications:
            # Prompt the user to save or discard changes before exiting
            choice = input("Do you want to save changes? (Y/N): ")
            if choice.upper() == "Y":
                self.save_changes()
            else:
                self.discard_changes()

        # Clear session-related data
        self.session_id = None
        self.modifications = []
        self.session_history = []


if __name__ == "__main__":
    pass
