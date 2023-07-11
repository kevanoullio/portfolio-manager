# Purpose: Database class for managing the database.

# Standard Libraries
import os
import shutil
import sqlite3

# Third-party Libraries

# Local Modules

# Class Definitions
class Database: # TODO prevent SQL injections in all SQL queries!!! 
    # TODO Rewrite all SQL queries to use ? instead of f-strings
    #  It's generally recommended to use parameterized queries with placeholders (? in SQLite)
    def __init__(self, db_filename: str):
        self.db_filename = db_filename
        self.connection = None
        self.cursor = None


    def open_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_filename)
                self.cursor = self.connection.cursor()
                print(f"{self.db_filename} database connection opened.")
            except sqlite3.Error as e:
                raise Exception(f"Error opening the {self.db_filename} database connection: {e}")
        else:
            print(f"{self.db_filename} database connection is already open.")


    def close_connection(self):
        if self.cursor is not None:
            try:
                self.cursor.close()
                self.cursor = None
                print(f"{self.db_filename} database cursor closed.")
            except sqlite3.Error as e:
                raise Exception(f"Error closing the {self.db_filename} database cursor: {e}")
        if self.connection is not None:
            try:
                self.connection.close()
                self.connection = None
                print(f"{self.db_filename} database connection closed.")
            except sqlite3.Error as e:
                raise Exception(f"Error closing the {self.db_filename} database connection: {e}")
        else:
            print(f"{self.db_filename} database connection or cursor are already closed.")


    def initialize_database(self, schema_filename: str) -> None:
        # TODO Check if initialization was successful, make sure the database file is deleted if it wasn't
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
            raise Exception(f"{self.db_filename} database connection is not open.")


    def __sanitize_input(self, input: str) -> str:
        # Remove any potentially dangerous characters
        sanitized_input = input.translate(str.maketrans('', '', '\'"<>;'))
        return sanitized_input


    def execute_query(self, query: str, params=None):
        print("Executing query:", query) # Print the query
        if self.connection is not None:
            if self.cursor is not None:
                try:
                    if params is None:
                        self.cursor.execute(query)
                    else:
                        self.cursor.execute(query, params)
                    self.connection.commit()
                    print("Query executed successfully.")
                    return self.cursor
                except sqlite3.Error as e:
                    raise Exception(f"Error executing query: {e}")
            else:
                raise Exception(f"Error executing query: {self.db_filename} cursor is None.")
        else:
            raise Exception(f"Error opening the {self.db_filename} database connection.")
        

    def table_exists(self, table_name: str) -> bool:
        # SQL query to check if a table exists
        check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        # Set the query parameters
        params = (table_name,)

        try:
            cursor = self.execute_query(check_table_query, params)
            result = cursor.fetchone()

            if result is not None:
                print(f"Table '{table_name}' exists.")
                return True
            else:
                print(f"Table '{table_name}' does not exist.")
                return False
        except sqlite3.Error as e:
            raise Exception(f"Error checking table existence: {e}")


    def table_empty(self, table_name: str) -> bool:
        # SQL query to check if a table is empty
        check_table_query = "SELECT * FROM ? LIMIT 1"
        # Set the query parameters
        params = (table_name,)

        # Execute the query
        cursor = self.execute_query(check_table_query, params)
        result = cursor.fetchone()

        if result is not None:
            print(f"Table '{table_name}' is not empty.")
            return False
        else:
            print(f"Table '{table_name}' is empty.")
            return True


    def column_exists(self, table_name: str, column_name: str) -> bool:
        # SQL query to check if a column exists
        check_column_query = f"SELECT count(*) FROM pragma_table_info('{table_name}') WHERE name='{column_name}'"
        # Set the query parameters
        params = (table_name, column_name)

        # Execute the query
        cursor = self.execute_query(check_column_query, params)
        result = cursor.fetchone()

        if result is not None:
            print(f"Column '{column_name}' exists.")
            return True
        else:
            print(f"Column '{column_name}' does not exist.")
            return False
        

    def store_username_and_password(self, username: str, password_hash: bytes) -> None:
        # SQL query to store the username and password hash
        store_username_and_password_query = "INSERT INTO user (username, password_hash) VALUES (?, ?)"
        # Set the query parameters
        params = (username, password_hash)
        
        try:
            # Execute the query
            self.execute_query(store_username_and_password_query, params)
            print(f"Username '{username}' and password hash stored.")
        except Exception as e:
            raise Exception(f"Error storing username and password: {e}")


    def get_user_id(self, username: str):
        # SQL query to get the user ID
        get_user_id_query = "SELECT id FROM user WHERE username = ?"
        # Set the query parameters
        params = (username,)

        # Execute the query
        cursor = self.execute_query(get_user_id_query, params)
        result = cursor.fetchone()

        if result is not None:
            return result[0]
        else:
            print(f"Username '{username}' does not exist.")
            return None
        

    def username_exists(self, username: str):
        # SQL query to check if a username exists
        check_username_query = "SELECT 1 FROM user WHERE username = ?"
        # Set the query parameters
        params = (username,)

        # Execute the query
        cursor = self.execute_query(check_username_query, params)
        result = cursor.fetchone()

        if result is not None:
            print(f"Username '{username}' exists.")
            return True
        else:
            print(f"Username '{username}' does not exist.")
            return False


    def check_table_exists(self, table_name: str) -> bool:
        # SQL query to check if the table exists
        check_table_query = "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?"
        # Return the count, 1 if the table exists and 0 if it does not
        return self.execute_check_query(check_table_query, (table_name,),
                f"Table '{table_name}' exists.",
                f"Table '{table_name}' does not exist.")


    def check_column_exists(self, table_name: str, column_name: str) -> bool:
        # SQL query to check if the column exists in the table
        check_column_query = "SELECT count(*) FROM pragma_table_info(?) WHERE name=?"
        # Return the count, 1 if the column exists and 0 if it does not
        return self.execute_check_query(check_column_query, (table_name, column_name),
                f"Column '{column_name}' exists in table '{table_name}'.",
                f"Column '{column_name}' does not exist in table '{table_name}'.")


    def check_entry_exists(self, table_name: str, condition: str, user_id: int) -> bool:
        # Sanitize the input to avoid SQL injection
        table_name = self.__sanitize_input(table_name)
        # condition = self.__sanitize_input(condition)

        # SQL query to check if the entry exists in the table
        check_entry_query = f"SELECT 1 FROM {table_name} WHERE {condition} AND user_id = ?"

        # Set the query parameters
        params = (user_id,)

        # Execute the query
        return self.execute_check_query(check_entry_query, params,
                f"Entry exists in table '{table_name}' with condition '{condition}'.",
                f"No entry exists in table '{table_name}' with condition '{condition}'.")


    def execute_check_query(self, query: str, params: tuple, success_message: str, failure_message: str) -> bool:
        # Execute the query
        cursor = self.execute_query(query, params)
        result = cursor.fetchone()

        # Print the appropriate message and return the result
        if result is not None:
            print(success_message)
            return True
        else:
            print(failure_message)
            return False


    def __get_allowable_table_names(self) -> list[str]:
        allowable_table_names = []

        with open("./database/schema.sql", "r") as file:
            schema = file.read()
            # Split the schema into lines
            lines = schema.split("\n")
            
            # Iterate over the lines
            for line in lines:
                line = line.strip()
                
                # Check if the line starts with "CREATE TABLE IF NOT EXISTS"
                if line.startswith("CREATE TABLE IF NOT EXISTS"):
                    # Extract the table name from the line
                    table_name = line.split()[5].strip("`")
                    allowable_table_names.append(table_name)
        
        return allowable_table_names


    def create_table(self, table_name: str, columns):
        # Join the column definitions
        column_definitions = ', '.join(columns)
        # SQL query to create a table
        create_table_query = "CREATE TABLE IF NOT EXISTS ? ({})".format(column_definitions)
        # Set the query parameters
        params = (table_name,)
        
        # Execute the query
        cursor = self.execute_query(create_table_query, params)
        result = cursor.fetchone()

        # Print the appropriate message
        if result is not None:
            print(f"Table '{table_name}' added successfully.")
        else:
            raise Exception(f"Error adding table '{table_name}'.")


    def add_column(self, table_name: str, column_definition):
        # SQL query to add a column to a table
        add_column_query = "ALTER TABLE ? ADD COLUMN ?"
        # Set the query parameters
        params = (table_name, column_definition)

        # Execute the query
        cursor = self.execute_query(add_column_query, params)
        result = cursor.fetchone()

        # Print the appropriate message
        if result is not None:
            print(f"Column '{column_definition}' added to table '{table_name}' successfully.")
        else:
            raise Exception(f"Error adding column '{column_definition}' to table '{table_name}'.") 


    def insert_entry(self, user_id: int, table_name: str, columns: list[str], values: list[str]):
        # Validate the table_name against allowed values
        allowed_table_names = self.__get_allowable_table_names()
        print(f"Allowed table names: {allowed_table_names}")
        print(f"Table name: {table_name}")
        if table_name not in allowed_table_names:
            raise Exception("Invalid table name.")

        # Join the column names and placeholders
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(values))

        # SQL query to insert an entry into a table
        insert_query = f"INSERT OR IGNORE INTO {table_name} (user_id, {columns_str}) VALUES (?, {placeholders})"
        # Set the query parameters
        params = [user_id] + values

        # Execute the query
        cursor = self.execute_query(insert_query, params)

        if cursor.rowcount > 0:
            print(f"Entry added to table '{table_name}' successfully.")
        else:
            raise Exception(f"Error adding entry to table '{table_name}'. Entry may already exist")


    def update_entry(self, table_name: str, columns, values, condition):
        # Join the column names
        columns_str = ', '.join([f"{column} = ?" for column in columns])
        # SQL query to update an entry in a table
        update_query = "UPDATE ? SET {} WHERE ?".format(columns_str)

        # Execute the query
        cursor = self.execute_query(update_query, (table_name, *values, condition))
        result = cursor.fetchone()

        # Print the appropriate message
        if result is not None:
            print(f"Entry updated in table '{table_name}' successfully.")
        else:
            raise Exception(f"Error updating entry in table '{table_name}'.")


    def execute_query_by_title(self, query_title: str, *args: str):
        # Read the queries.sql file
        with open("queries.sql", "r") as file:
            queries = file.read()

        # Find the selected query by matching the title
        selected_query = self.__find_query_by_title(queries, query_title)

        # Execute the selected query with variable substitution
        if selected_query:
            query_with_values = self.__replace_variables(selected_query, args)
            # Execute the query
            cursor = self.execute_query(query_with_values)
            result = cursor.fetchone()

            # Print the appropriate message and return the result
            if result is not None:
                print(f"Query '{query_title}' executed successfully.")
                return result
            else:
                return None


    def __find_query_by_title(self, queries: str, query_title: str):
        individual_queries = queries.split(";")
        for query in individual_queries:
            query = query.strip()
            if query.startswith("--"):
                comment = query[2:].strip()
                if query_title in comment:
                    return individual_queries[individual_queries.index(query) + 1]
        return None


    def __replace_variables(self, query: str, args) -> str:
        for arg in args:
            query = query.replace("?", arg, 1)
        return query

        
    def get_password_hash(self, username: str) -> bytes:
        # SQL query to get the password hash for a username
        get_password_hash_query = "SELECT password_hash FROM user WHERE username = ?"
        # Set the query parameters
        params = (username,)
        
        # Execute the query
        cursor = self.execute_query(get_password_hash_query, params)
        result = cursor.fetchone()

        # Print the appropriate message and return the result
        if result is not None:
            return result[0]
        else:
            print(f"Username '{username}' does not exist.")
            return result


    def import_custom_script(self, menu_options: list) -> None:
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


    def __get_email_usage_id(self, email_usage: str) -> int:
        # SQL query to get the email usage id
        get_email_usage_id_query = "SELECT id FROM email_usage WHERE usage = ?"
        # Set the query parameters
        params = (email_usage,)

        # Execute the query
        cursor = self.execute_query(get_email_usage_id_query, params)
        result = cursor.fetchone()

        # Print the appropriate message and return the result
        if result is not None:
            return result[0]
        else:
            print(f"Email usage '{email_usage}' does not exist.")
            return result


    def fetch_email_accounts(self, user_id: int, email_usage: str) -> list:
        # Get the email usage id
        email_usage_id = self.__get_email_usage_id(email_usage)
        # Define the SQL query, ensure only emails associated with currently logged in user are displayed
        fetch_email_accounts_query = "SELECT email_address FROM email WHERE user_id = ? AND email_usage_id = ?"
        print(f"fetch_email_accounts_query: {fetch_email_accounts_query}")
        # Set the query parameters
        params = (user_id, email_usage_id)
        print(f"params: {params}")

        # Execute the query
        cursor = self.execute_query(fetch_email_accounts_query, params)
        # result = cursor.fetchall()
        result = cursor.fetchone()
        # result = [row[0] for row in cursor.fetchall()]
        print(f"result: {result}")

        # Print the appropriate message and return the result
        if result:
            print(f"Email accounts fetched successfully.")
        else:
            print(f"Error fetching email accounts.")

        return result


    def get_data_type_id(self, user_id: int, data_type: str) -> int:
        # SQL query to get the id of a data type
        get_data_type_id_query = "SELECT id FROM data_type WHERE user_id = ? AND name = ?"
        # Set the query parameters
        params = (user_id, data_type)

        # Execute the query
        cursor = self.execute_query(get_data_type_id_query, params)
        result = cursor.fetchone()

        # Print the appropriate message and return the result
        if result is not None:
            print(f"Data type '{data_type}' fetched successfully.")
            return result[0]
        else:
            print(f"Error fetching data type '{data_type}'.")
            return result
    

    def import_file(self, user_id: int, file_type: str, file_extensions: list[str]) -> None:
        # Only allow importing .db database files
        print(f"allowed file types: {file_extensions}")
        # Prompt the user for the file path
        filepath = input(f"Enter the path to the {file_type} file: ")

        # Check if the file exists
        if not os.path.isfile(filepath):
            print("The file does not exist.")
            return

        # Format the file name
        data_name = os.path.basename(filepath)

        # Columns to insert into the data_type table
        columns = ["[name]"]
        # Values to insert into the data_type table
        values = [file_type]

        # Add the data type to the data_type table
        try:
            self.insert_entry(user_id, "data_type", columns, values)
        except sqlite3.IntegrityError:
            print("Error: Data type already exists.")
            return 

        # Get the data type id
        data_type_id = self.get_data_type_id(user_id, file_type)

        # Columns to insert into the imported_data table
        columns = ["user_id", "[name]", "data_type_id", "filepath"]
        # Values to insert into the imported_data table
        values = [str(user_id), data_name, str(data_type_id), filepath]

        # Add the file to the imported_data table
        self.insert_entry(user_id, "imported_data", columns, values)
        
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


if __name__ == "__main__":
    db = Database("database.db")
    db.initialize_database("./database/schema.sql")
