# Purpose: Database class for managing the database.

# Standard Libraries
import copy
import os
import shutil
import sqlite3

# Third-party Libraries

# Local Modules
from data_management.connection import DatabaseConnection
from data_management.query.query_executor import QueryExecutor
from data_management.schema.schema import DatabaseSchema

# Configure logging
import logging


# Database class for managing the database
class Database: # TODO prevent SQL injections in all SQL queries!!! 
    # TODO - Rewrite all SQL queries to use ? instead of f-strings
    #  It's generally recommended to use parameterized queries with placeholders (? in SQLite)
    def __init__(self, db_filename: str):
        self.db_filename = db_filename
        self.db_schema = DatabaseSchema(self.db_connection)
        self.query_executor = QueryExecutor(self.db_connection)
        logging.info(f"Database initialized. Database: {self.db_filename}")

    # TODO - all executions that return data don't need to commit the transaction?
    # TODO - call begin_transaction() then execute then commit_transaction() for transactions
    # self.db_connection.commit_transaction()
    def initialize(self, schema_filename: str) -> None:
        self.db_schema.initialize_database(schema_filename)

    def set_session_manager(self, session_manager) -> None:
        self.session_manager = session_manager



    def with_connection(self, callback):
        # Create a new instance of the Connection class
        db_connection = DatabaseConnection(self.db_filename)
        # Open the database connection
        db_connection.open_connection()
        # Call the callback function, passing in the open connection
        result = callback(db_connection)
        # Close the database connection
        db_connection.close_connection
        return result

    def execute_query(self, query):
        # Execute a query using the query executor
        return self.query_executor.execute_query(query)







    def restore(self, snapshot_data) -> None:
        # Implement the logic to restore the database to the state of the given snapshot
        # You would typically need to perform operations such as truncating tables,
        # restoring data from the snapshot, etc.
        # Make sure to handle any necessary error checking and transaction management.

        # Example: Assuming you have a snapshot of the entire database,
        # you can replace the existing database file with the snapshot file
        snapshot_filename = snapshot_data.get_snapshot_filename()
        shutil.copyfile(snapshot_filename, self.db_filename)








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

    def import_file(self, user_id: int, file_type: str, file_extensions: list[str]) -> None:
        # Only allow importing .db database files
        print(f"Allowed file types: {file_extensions}")
        # Prompt the user for the file path
        filepath = input(f"Enter the path to the {file_type} file: ")

        # Check if the file exists
        if not os.path.isfile(filepath):
            print("The file does not exist.")
            return

        # Format the file name
        data_name = os.path.basename(filepath)

        # Columns to insert into the data_type table
        columns = ("[name]",)
        # Values to insert into the data_type table
        values = (file_type,)

        # Add the data type to the data_type table
        try:
            self.insert_entry("data_type", columns, values, user_id)
        except sqlite3.IntegrityError:
            print("Error: Data type already exists.")
            return 

        # Get the data type id
        data_type_id = self.query_executor.get_data_type_id(user_id, file_type)

        # Columns to insert into the imported_data table
        columns = ("[name]", "data_type_id", "filepath")
        # Values to insert into the imported_data table
        values = (data_name, data_type_id, filepath)

        # Add the file to the imported_data table
        self.insert_entry("imported_data", columns, values, user_id)
        
        # Define the destination directory
        destination_dir = f"./user_data/{file_type}/"
        # Create the destination directory if it doesn't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        # Copy the file to the destination directory
        shutil.copy(filepath, destination_dir)
        print("Database file imported successfully.")


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
