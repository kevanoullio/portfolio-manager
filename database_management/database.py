# Purpose: Database class for managing the database.

# Standard Libraries
import copy
import os
import shutil
import sqlite3

# Third-party Libraries
import pandas as pd

# Local Modules
from database_management.connection import DatabaseConnection, DatabaseConnectionError
from session_management.session_manager import SessionManager
from database_management.query.query_executor import QueryExecutor
from database_management.schema.schema import DatabaseSchema
from database_management.backup import BackupManager

# Configure logging
import logging


# Database class for managing the database
class Database: # TODO prevent SQL injections in all SQL queries!!! 
    # TODO - Rewrite all SQL queries to use ? instead of f-strings
    #  It's generally recommended to use parameterized queries with placeholders (? in SQLite)
    def __init__(self, db_filename: str, db_schema_filename: str):
        self._db_filename = db_filename
        self._db_schema_filename = db_schema_filename
        self._db_connection = DatabaseConnection(db_filename)
        self._backup_manager = BackupManager(self._db_filename)
        self.session_manager = SessionManager()
        self.query_executor = QueryExecutor(self._db_connection, self.session_manager)

    def start(self) -> None:
        # Check if the database file exists
        if os.path.exists(self._db_filename):
            # Check if a backup file exists
            if os.path.exists(self._backup_manager.db_backup_filename):
                logging.info("Backup file exists.")
            else:
                print("Backup file does not exist.")
                logging.info("Backup file does not exist.")
                # Create a new backup database file and initialize it
                self._backup_manager.create_backup()
        else:
            print("Database file does not exist.")
            logging.info("Database file does not exist.")
            # Check if a backup file exists
            if os.path.exists(self._backup_manager.db_backup_filename):
                print("Backup file exists.")
                logging.info("Backup file exists.")
                # Restore from the backup file
                self._backup_manager.restore_from_backup()
            else:
                print("Initializing new database file...")
                logging.info("Initializing new database file...")
                # Create a new database file by opening and closing a connection
                # Create a Database Schema object and initialize the database using the schema file
                db_schema = DatabaseSchema(self.query_executor, self._db_schema_filename)
                db_schema.initialize_database()
                print(f"Database file created and initialized successfully.")
                logging.info(f"Database file created and initialized successfully. Database: {self._db_filename}")
                if os.path.exists(self._backup_manager.db_backup_filename):
                    logging.info("Backup file exists.")
                else:
                    print("Backup file does not exist.")
                    logging.info("Backup file does not exist.")
                    # Create a new backup database file and initialize it
                    self._backup_manager.create_backup()

    def restore(self, snapshot_data) -> None:
        # Implement the logic to restore the database to the state of the given snapshot
        # You would typically need to perform operations such as truncating tables,
        # restoring data from the snapshot, etc.
        # Make sure to handle any necessary error checking and transaction management.

        # Example: Assuming you have a snapshot of the entire database,
        # you can replace the existing database file with the snapshot file
        snapshot_filename = snapshot_data.get_snapshot_filename()
        shutil.copyfile(snapshot_filename, self._db_filename)

    def import_custom_script(self, menu_options: dict) -> None:
        # Only allow importing python scripts
        print("allowed scripts: [.py]")
        # Prompt the user for the script file path
        script_path = input("Enter the path to the script file: ")

        # Check if the file exists
        if not os.path.isfile(script_path):
            print("The file does not exist.")
            return
        
        # Define the destination directory
        destination_dir = "./user_data/scripts/"
        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Copy the file to the destination directory
        shutil.copy(script_path, destination_dir)

        # Format the file name
        script_name = os.path.basename(script_path)

        # # Add the script to the menu options
        # menu_options.append(script_name)
        print("Script imported successfully.")

    # # FIXME - fix this function to work with new code
    # def import_file(self, user_id: int, file_type: str, file_extensions: list[str]) -> None:
    #     # Only allow importing .db database files
    #     print(f"Allowed file types: {file_extensions}")
    #     # Prompt the user for the file path
    #     filepath = input(f"Enter the path to the {file_type} file: ")

    #     # Check if the file exists
    #     if not os.path.isfile(filepath):
    #         print("The file does not exist.")
    #         return

    #     # Format the file name
    #     data_name = os.path.basename(filepath)

    #     # Columns to insert into the data_type table
    #     columns = ("[name]",)
    #     # Values to insert into the data_type table
    #     values = (file_type,)

    #     # Add the data type to the data_type table
    #     try:
    #         self.query_builder.insert_entry("data_type", columns, values, user_id)
    #     except sqlite3.IntegrityError:
    #         print("Error: Data type already exists.")
    #         return 

    #     # Get the data type id
    #     data_type_id = self.query_executor.get_data_type_id(user_id, file_type)

    #     # Columns to insert into the imported_data table
    #     columns = ("[name]", "data_type_id", "filepath")
    #     # Values to insert into the imported_data table
    #     values = (data_name, data_type_id, filepath)

    #     # Add the file to the imported_data table
    #     self.query_builder.insert_entry("imported_data", columns, values, user_id)
        
    #     # Define the destination directory
    #     destination_dir = f"./user_data/{file_type}/"
    #     # Create the destination directory if it doesn't exist
    #     if not os.path.exists(destination_dir):
    #         os.makedirs(destination_dir)
    #     # Copy the file to the destination directory
    #     shutil.copy(filepath, destination_dir)
    #     print("Database file imported successfully.")


    # def add_email_address(self, user_id: int, email: str, usage: str):
    #     pass

    # def add_email_password_hash(self, user_id: int, email_password_hash: str):
    #     pass


# DatabaseSnapshot class for managing database snapshots
class DatabaseSnapshot:
    def __init__(self, database: Database) -> None:
        self.data = copy.deepcopy(database)  # Make a copy of the database at this point

    def rollback(self, database: Database) -> None:
        # Restore the database to the state of this snapshot
        database.restore(self.data)


# SnapshotData class for storing snapshot IDs and retrieving snapshot filenames
class SnapshotData:
    def __init__(self, snapshot_id):
        self.snapshot_id = snapshot_id

    def get_snapshot_filename(self):
        # Implement the logic to retrieve the snapshot filename based on the snapshot_id
        # This could involve constructing the filename using the snapshot_id or querying a database/file system

        # Example: Assuming the snapshot files are stored in a directory with the format "snapshot_{snapshot_id}.db"
        filename = f"snapshot_{self.snapshot_id}.db"
        return filename


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
