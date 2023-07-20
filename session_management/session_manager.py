# Purpose: Session Manager module for managing the current session state.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# SessionManager class for managing the current user session
class SessionManager:
    def __init__(self):
        self._current_user: UserAccount | None = None
        self._session_token: str | None = None
        self.modifications = []
        self.session_history = []
        logging.info("Session Manager initialized.")

    def get_current_user(self) -> UserAccount | None:
        return self._current_user
    
    def set_current_user(self, current_user: UserAccount | None) -> None:
        self._current_user = current_user

    def get_current_user_id(self) -> int:
        current_user = self.get_current_user()
        if current_user is None:
            return 0
        else:
            return current_user.user_id

    def get_session_token(self) -> str | None:
        return self._session_token
    
    def set_session_token(self, session_token: str | None) -> None:
        self._session_token = session_token

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
