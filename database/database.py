# Purpose: Database class for managing the database.

# Standard Libraries
import sqlite3

# Third-party Libraries


# Local Modules


# Class Definitions
class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None


    def initialize_database(self):
        # Check if the user table exists
        if not self.is_table_exists("users"):
            # If the user table does not exist, create it
            self.create_user_table()
        else:
            # If the user table exists, do nothing
            pass


    def open_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_file)
                print("Database connection opened.")
            except sqlite3.Error as e:
                raise Exception(f"Error opening the database connection: {e}")
        else:
            print("Database connection is already open.")


    def close_connection(self):
        if self.connection is not None:
            try:
                self.connection.close()
                print("Database connection closed.")
            except sqlite3.Error as e:
                raise Exception(f"Error closing the database connection: {e}")
        else:
            print("Database connection is already closed.")


    def is_table_exists(self, table_name):
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


    def create_user_table(self):
        if self.connection is not None:
            # SQL statement to create a user table
            create_table_query = """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            """
            self.connection.execute(create_table_query)
            self.connection.commit()
            print("User table created.")
        else:
            raise Exception("Database connection is not open.")


    def store_username_and_password(self, username, password):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    db = Database('database.db')
    db.initialize_database()
