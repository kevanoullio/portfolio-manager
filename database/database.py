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


    def column_exists(self, table_name: str, column_name: str) -> bool:
        # SQL query to check if a column exists
        check_column_query = f"SELECT count(*) FROM pragma_table_info('{table_name}') WHERE name='{column_name}'"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(check_column_query)
                result = cursor.fetchone()

                if result is not None:
                    print(f"Column '{column_name}' exists.")
                    return True
                else:
                    print(f"Column '{column_name}' does not exist.")
                    return False
            except sqlite3.Error as e:
                raise Exception(f"Error checking column existence: {e}")
        else:
            raise Exception("Error opening the database connection.")
        

    def store_username_and_password(self, username: str, password_hash: str) -> None:
        # SQL query to store a username and password hash
        store_username_and_password_query = "INSERT INTO user (username, password_hash) VALUES (?, ?)"
        
        # Check if the connection is open
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(store_username_and_password_query, (username, password_hash))
                self.connection.commit()
                print(f"Username '{username}' and password hash stored.")
            except sqlite3.Error as e:
                raise Exception(f"Error storing username and password hash: {e}")
        else:
            raise Exception("Error opening the database connection.")


    def get_user_id(self, username: str):
        # SQL query to get the user ID for a username
        get_user_id_query = f"SELECT id FROM user WHERE username='{username}'"

        # Check if the connection is open
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(get_user_id_query)
                result = cursor.fetchone()

                if result is not None:
                    return result[0]
                else:
                    print(f"Username '{username}' does not exist.")
                    return None
            except sqlite3.Error as e:
                raise Exception(f"Error getting user ID: {e}")
        else:
            raise Exception("Error opening the database connection.")
        

    def username_exists(self, username: str):
        # SQL query to check if a username exists
        check_username_query = f"SELECT username FROM user WHERE username='{username}'"

        # Check if the connection is open
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





    def check_table_exists(self, table_name: str) -> bool:
        check_table_query = f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        return self.execute_check_query(check_table_query,
            f"Table '{table_name}' exists.",
            f"Table '{table_name}' does not exist.")


    def check_column_exists(self, table_name: str, column_name: str) -> bool:
        check_column_query = f"PRAGMA table_info({table_name})"
        return self.execute_check_query(check_column_query,
            f"Column '{column_name}' exists in table '{table_name}'.",
            f"Column '{column_name}' does not exist in table '{table_name}'.")


    def check_entry_exists(self, table_name: str, condition: str, user_id: int) -> bool:
        check_entry_query = f"SELECT 1 FROM {table_name} WHERE {condition} AND user_id = {user_id}"
        return self.execute_check_query(check_entry_query,
            f"Entry exists in table '{table_name}' with condition '{condition}'.",
            f"No entry exists in table '{table_name}' with condition '{condition}'.")


    def execute_check_query(self, query: str, success_message: str, failure_message: str) -> bool:
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                result = cursor.fetchone()

                if result is not None:
                    print(success_message)
                    return True
                else:
                    print(failure_message)
                    return False
            except sqlite3.Error as e:
                raise Exception(f"Error executing check query: {e}")
        else:
            raise Exception("Database connection is not open.")







    def add_table(self, table_name: str, columns: list[str]) -> None:
        add_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.execute_query(add_table_query,
            f"Table '{table_name}' added successfully.")


    def add_column(self, table_name: str, column_definition: str) -> None:
        add_column_query = f"ALTER TABLE {table_name} ADD COLUMN {column_definition}"
        self.execute_query(add_column_query,
            f"Column '{column_definition}' added to table '{table_name}' successfully.")


    def add_entry(self, table_name: str, columns: list[str], values: list[str]) -> None:
        columns_str = ', '.join(columns)
        values_str = ', '.join([f"'{value}'" for value in values])
        add_entry_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"
        self.execute_query(add_entry_query,
            f"Entry added to table '{table_name}' successfully.")


    def execute_query(self, query: str, success_message: str) -> None:
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
                print(success_message)
            except sqlite3.Error as e:
                raise Exception(f"Error executing query: {e}")
        else:
            raise Exception("Database connection is not open.")








    def get_password_hash(self, username: str) -> str:
        # SQL query to get the password hash for a username
        get_password_hash_query = "SELECT password_hash FROM user WHERE username=?"

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                cursor.execute(get_password_hash_query, (username))
                result = cursor.fetchone()

                if result is not None:
                    return result[0]
                else:
                    print(f"Username '{username}' does not exist.")
                    return result
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


    # def add_email_address(self, user_id: int, email: str, usage: str):
    #     # Check if the usage already exists in the email_usage table
    #     if not self.check_entry_exists("email_usage", f"usage='{usage}'"):
    #         # Add the usage to the email_usage table
    #         self.add_email_usage(usage)
    #     if not self.email_usage_exists(usage):

    #     # Define the SQL query, ensure email is associated with currently logged in user
    #     add_email_address_query = f'''
    #         INSERT INTO user_email (user_id, email_address, email_usage_id)
    #         VALUES ({user_id}, '{email}', (SELECT id FROM email_usage WHERE usage = '{usage}'))
    #     '''

    #     # Check if the connection is open
    #     if self.connection is not None:
    #         try:
    #             # Execute the query
    #             cursor = self.connection.cursor()
    #             cursor.execute(add_email_address_query)
    #             self.connection.commit()
    #             print(f"Email address '{email}' added.")
    #         except sqlite3.Error as e:
    #             raise Exception(f"Error adding email address: {e}")
    #     else:
    #         raise Exception("Database connection is not open.")


    # def add_email_password_hash(self, user_id: int, email_password_hash: str):
    #     pass


    def fetch_email_accounts(self, user_id: int) -> list:
        # Define the SQL query, ensure only emails associated with currently logged in user are displayed
        fetch_email_accounts_query = f'''
            SELECT email FROM user
            WHERE id = {user_id}
        '''

        # Check if the connection is open
        if self.connection is not None:
            try:
                # Execute the query
                cursor = self.connection.cursor()
                cursor.execute(fetch_email_accounts_query)
                result = cursor.fetchall()

                return result
            except sqlite3.Error as e:
                raise Exception(f"Error displaying email accounts: {e}")
        else:
            raise Exception("Database connection is not open.")


if __name__ == "__main__":
    db = Database("database.db")
    db.initialize_database("./database/schema.sql")
