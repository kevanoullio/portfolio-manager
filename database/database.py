# Purpose: Database class for managing the database.

# Standard Libraries
import os
import shutil
import sqlite3

# Third-party Libraries


# Local Modules


# Class Definitions
class Database: #TODO prevent SQL injections in all SQL queries!!!
    def __init__(self, db_filename: str):
        self.db_filename = db_filename
        self.connection = None
        self.cursor = None


    def open_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_filename)
                self.cursor = self.connection.cursor()
                print("Database connection opened.")
            except sqlite3.Error as e:
                raise Exception(f"Error opening the database connection: {e}")
        else:
            print("Database connection is already open.")


    def close_connection(self):
        if self.cursor is not None:
            try:
                self.cursor.close()
                print("Database cursor closed.")
            except sqlite3.Error as e:
                raise Exception(f"Error closing the database cursor: {e}")
        if self.connection is not None:
            try:
                self.connection.close()
                print("Database connection closed.")
            except sqlite3.Error as e:
                raise Exception(f"Error closing the database connection: {e}")
        else:
            print("Database connection is already closed.")


    def initialize_database(self, schema_filename: str) -> None:
        # Read the schema file
        with open(schema_filename, 'r') as schema_file:
            schema_sql = schema_file.read()

        # Check if the connection is open
        if self.connection is not None:
            # Execute the schema SQL statements
            self.connection.executescript(schema_sql)
            # Commit the changes
            self.connection.commit()
        else:
            raise Exception("Database connection is not open.")


    def table_exists(self, table_name):
        # SQL query to check if a table exists
        check_table_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(check_table_query)
                result = cursor.fetchone()

                if result is not None:
                    print(f"Table '{table_name}' exists.")
                    return True
                else:
                    print(f"Table '{table_name}' does not exist.")
                    return False
            except sqlite3.Error as e:
                raise Exception(f"Error checking table existence: {e}")
        else:
            raise Exception("Error opening the database connection.")


    def table_empty(self, table_name):
        # SQL query to check if a table is empty
        check_table_query = f"SELECT * FROM {table_name}"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(check_table_query)
                result = cursor.fetchone()

                if result is not None:
                    print(f"Table '{table_name}' is not empty.")
                    return False
                else:
                    print(f"Table '{table_name}' is empty.")
                    return True
            except sqlite3.Error as e:
                raise Exception(f"Error checking table emptiness: {e}")
        else:
            raise Exception("Error opening the database connection.")


    def store_username_and_password(self, username: str, password: str):
        conn = sqlite3.connect(self.db_filename)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (username, password_hash) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        conn.close()


    def username_exists(self, username: str):
        # SQL query to check if a username exists
        check_username_query = f"SELECT username FROM user WHERE username='{username}'"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(check_username_query)
                result = cursor.fetchone()

                if result is not None:
                    print(f"Username '{username}' exists.")
                    return True
                else:
                    print(f"Username '{username}' does not exist.")
                    return False
            except sqlite3.Error as e:
                raise Exception(f"Error checking username existence: {e}")
        else:
            raise Exception("Error opening the database connection.")


    def get_password_hash(self, username: str):
        # SQL query to get the password hash for a username
        get_password_hash_query = f"SELECT password_hash FROM user WHERE username='{username}'"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(get_password_hash_query)
                result = cursor.fetchone()

                if result is not None:
                    return result[0]
                else:
                    print(f"Username '{username}' does not exist.")
                    return None
            except sqlite3.Error as e:
                raise Exception(f"Error getting password hash: {e}")
        else:
            raise Exception("Error opening the database connection.")


    def import_custom_script(self, menu_options: list):
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

        # Add the script to the menu options
        menu_options.append(script_name)
        print("Script imported successfully.")


if __name__ == "__main__":
    db = Database("database.db")
    db.initialize_database("./database/schema.sql")
