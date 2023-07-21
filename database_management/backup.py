# Purpose: Backup module for creating and restoring database backups.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries
import shutil
import sqlite3

# Third-party Libraries

# Local Modules
from database_management.schema.schema import DatabaseSchema

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from database_management.database import DatabaseConnection

# Configure logging
import logging


# BackupManager class for creating and restoring database backups
class BackupManager:
    def __init__(self, db_filename: str) -> None:
        self.db_filename: str = db_filename
        self.db_backup_filename: str = f"{self.db_filename}.bak"

    def restore_from_backup(self) -> bool:
        try:
            # Restore from the backup by copying the backup file to the database file
            shutil.copyfile(self.db_backup_filename, self.db_filename)
            logging.info("Backup file restored.")
            return True
        except (IOError, shutil.Error) as e:
            print(f"Failed to restore from backup: {str(e)}")
            return False

    def create_backup(self) -> bool:
        try:
            # Create a new backup by copying the database file
            shutil.copyfile(self.db_filename, self.db_backup_filename)
            logging.info("Backup file created.")
            return True
        except (IOError, shutil.Error) as e:
            print(f"Failed to restore from backup: {str(e)}")
            return False


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
