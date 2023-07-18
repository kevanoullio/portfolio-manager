# Purpose: Session Manager module for managing the current session state.

# Standard Libraries


# Third-party Libraries

# Local Modules
from account_management.user_account import UserAccount
# Import all remaining local modules using lazy imports to avoid circular importing

# Configure logging
import logging


# SessionManager class for managing the current user session
class SessionManager:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.current_user: UserAccount | None = None
        self.logged_in: bool = False
        self.session_token: str | None = None
        self.modifications = []
        self.session_history = []
        logging.info("Session Manager initialized.")


    def initialize_modules(self):
        # Import all local modules here to avoid circular importing
        from data_management.database import Database, DatabaseSnapshot
        from data_management.queries import QueryExecutor
        from user_interface.dashboard import Dashboard
        from access_management.login_manager import LoginManager
        from access_management.account_authenticator import AccountAuthenticator
        from session_management.token_manager import SessionTokenManager


        self.database = Database(self.db_filename)
        self.query_executor = QueryExecutor(self.database.db_connection)
        self.dashboard = Dashboard()
        self.login_manager = LoginManager()
        self.account_authenticator = AccountAuthenticator()
        self.session_token_manager = SessionTokenManager()


    def set_session_manager(self, session_manager):
        self.database.set_session_manager(session_manager)
        self.query_executor.set_session_manager(session_manager)
        self.dashboard.set_session_manager(session_manager)
        self.login_manager.set_session_manager(session_manager)
        self.account_authenticator.set_session_manager(session_manager)
        self.session_token_manager.set_session_manager(session_manager)


    def start_session(self) -> None:
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
        self.modifications = []
        self.session_history = []
        


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
