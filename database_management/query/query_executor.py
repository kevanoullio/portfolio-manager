# Purpose: Database Queries class for executing SQL statements.

# Standard Libraries
import sqlite3

# Third-party Libraries

# Local Modules
from account_management.accounts import UserAccount, EmailAccount
from database_management.connection import DatabaseConnection, DatabaseConnectionError
from session_management.session_manager import SessionManager

# Configure logging
import logging


# QueryExecutor class for executing SQL statements
class QueryExecutor:
    def __init__(self, db_connection: DatabaseConnection, session_manager: SessionManager):
        self.db_connection = db_connection
        self.session_manager = session_manager
        self.complex_queries_file = "./data_management/complex_queries.sql"
        logging.info(f"Query executor initialized. Database: {self.db_connection.db_filename}")

    def execute_query(self, query: str, params: tuple[str] | None = None) -> list[tuple] | None:
        try:
            with self.db_connection as connection:
                with connection.cursor() as cursor:
                    if params is not None:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    return cursor.fetchall()
        except DatabaseConnectionError as e:
            logging.error(str(e))
            raise DatabaseQueryError(self.db_connection, "Error executing the database query", e)
        except sqlite3.Error as e:
            logging.error(f"Error executing the database query: {str(e)}")
            raise DatabaseQueryExecutionError(self.db_connection, "SQL", e)

    def __find_complex_query_by_title(self, queries: str, query_title: str) -> str | None:
        individual_queries = queries.split(";")
        for i, query in enumerate(individual_queries):
            query = query.strip()
            query = query
            print(f"query: {query}")
            if query_title in query:
                print(f"Found query: {individual_queries[i].strip()}")
                return individual_queries[i].strip()
            # if query.startswith(" --"):
            #     comment = query[2:].strip()
            #     print(f"comment: {comment}")
            #     if query_title in comment:
            #         print(f"Found query: {individual_queries[i + 1].strip()}")
            #         return individual_queries[i + 1].strip()
        return None

    def __replace_variables(self, query: str, args) -> str:
        for arg in args:
            query = query.replace("?", arg, 1)
        return query

    def execute_complex_query_by_title(self, query_title: str, *args: str) -> list[tuple] | None:
        # Read the complex_queries.sql file
        with open(self.complex_queries_file, "r") as file:
            queries = file.read()

        # Find the selected query by matching the title
        selected_query = self.__find_complex_query_by_title(queries, query_title)

        # Execute the selected query with variable substitution
        if selected_query:
            query_with_values = self.__replace_variables(selected_query, args)
            # Execute the query
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(query_with_values)
                    result = cursor.fetchall()  # Fetch all rows of the result
                    return result
            except Exception as e:
                raise DatabaseQueryExecutionError(self.db_connection, "QUERY BY TITLE", e)
        else:
            raise DatabaseQueryError(self.db_connection, f"Query with title '{query_title}' not found.")




# Create Table: Creating a new table in the database.
# Drop Table: Removing an existing table from the database.
# Rename Table: Renaming an existing table in the database.
# Add Column: Adding a new column to an existing table.
# Alter Column: Modifying the properties or attributes of an existing column in a table.
# Drop Column: Removing a column from an existing table.
# Insert: Adding a new entry/row to a table.
# Update: Modifying existing entries/rows in a table.
# Delete: Removing entries/rows from a table.
# Select: Retrieving data from one or more tables.
# Join: Combining data from multiple tables based on a related column.
# Index: Creating an index on one or more columns to improve query performance.
# View: Virtual table that is based on the result of a SQL query.
# Trigger: Special type of stored procedure that is automatically executed when a certain event occurs, such as an insert, update, or delete operation.
# Constraint: Defining rules or conditions that the data must adhere to, such as primary keys, foreign keys, unique constraints, etc.
# Transaction: Grouping multiple queries into a single atomic unit of work that should either succeed or fail as a whole.
# Stored Procedure: Predefined set of SQL statements that can be executed as a single unit.

    # TODO - review all of this code and consolidate into query_builder
    def create_table(self, table_name: str, columns: tuple[str]) -> None:
        query_type = "CREATE TABLE"
        query = f"{query_type} IF NOT EXISTS {table_name} {columns}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def rename_table(self, table_name: str, new_table_name: str) -> None:
        query_type = "ALTER TABLE"
        query = f"{query_type} {table_name} RENAME TO {new_table_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def drop_table(self, table_name: str) -> None:
        query_type = "DROP TABLE"
        query = f"{query_type} IF EXISTS {table_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
        query_type = "ADD COLUMN"
        query = f"ALTER TABLE {table_name} {query_type} {column_name} {data_type}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def rename_column(self, table_name: str, column_name: str, new_column_name: str) -> None:
        query_type = "RENAME COLUMN"
        query = f"ALTER TABLE {table_name} {query_type} {column_name} TO {new_column_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def alter_column(self, table_name: str, column_name: str, new_data_type: str) -> None:
        query_type = "ALTER COLUMN"
        query = f"ALTER TABLE {table_name} {query_type} {column_name} {new_data_type}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def drop_column(self, table_name: str, column_name: str) -> None:
        query_type = "DROP COLUMN"
        query = f"ALTER TABLE {table_name} {query_type} {column_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def insert_entry(self, table_name: str, columns: tuple, values: tuple, user_id: int) -> None:
        query_type = "INSERT"
        query = f"{query_type} INTO {table_name} {columns} VALUES {values} WHERE user_id = {user_id}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def update_entry(self, table_name: str, column_name: str, new_value: str, where_clause: str, user_id: int) -> None:
        query_type = "UPDATE"
        query = f"{query_type} {table_name} SET {column_name} = {new_value} WHERE {where_clause} AND user_id = {user_id}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def delete_entry(self, table_name: str, columns: tuple, values: tuple, user_id: int) -> None:
        query_type = "DELETE"
        query = f"{query_type} FROM {table_name} WHERE {columns} = {values} AND user_id = {user_id}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def select(self, table_name: str, columns: tuple[str], user_id: int, where_clause: str | None = None) -> list[dict[str, str]]:
        query_type = "SELECT"
        query = f"{query_type} {columns} FROM {table_name}"
        if where_clause is not None:
            query += f" WHERE {where_clause} AND user_id = {user_id}"
        else:
            query += f" WHERE user_id = {user_id}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def join(self, table_name_1: str, table_name_2: str, columns: tuple[str], join_condition: str, user_id: int) -> list[dict[str, str]]:
        query_type = "JOIN"
        query = f"{query_type} {table_name_1} INNER JOIN {table_name_2} ON {join_condition} {columns} WHERE user_id = {user_id}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_index(self, table_name: str, column_name: str) -> None:
        query_type = "CREATE INDEX"
        query = f"{query_type} ON {table_name} ({column_name})"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def drop_index(self, table_name: str, column_name: str) -> None:
        query_type = "DROP INDEX"
        query = f"{query_type} {table_name} {column_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def create_view(self, view_name: str, view_body: str) -> None:
        query_type = "VIEW"
        query = f"{query_type} {view_name} {view_body}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def drop_view(self, view_name: str) -> None:
        query_type = "DROP VIEW"
        query = f"{query_type} {view_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_trigger(self, trigger_name: str, trigger_body: str) -> None:
        query_type = "TRIGGER"
        query = f"{query_type} {trigger_name} {trigger_body}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def drop_trigger(self, trigger_name: str) -> None:
        query_type = "DROP TRIGGER"
        query = f"{query_type} {trigger_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_constraint(self, table_name: str, constraint_type: str, column_name: str) -> None:
        query_type = "CREATE CONSTRAINT"
        query = f"{query_type} {constraint_type} {table_name} {column_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def drop_constraint(self, table_name: str, constraint_type: str, column_name: str) -> None:
        query_type = "DROP CONSTRAINT"
        query = f"{query_type} {constraint_type} {table_name} {column_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_transaction(self, queries: list[str]) -> None:
        query_type = "TRANSACTION"
        try:
            with self.db_connection.cursor() as cursor:
                for query in queries:
                    cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_stored_procedure(self, procedure_name: str, procedure_body: str) -> None:
        query_type = "STORED PROCEDURE"
        query = f"{query_type} {procedure_name} {procedure_body}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def call_stored_procedure(self, procedure_name: str, procedure_arguments: tuple[str]) -> None:
        query_type = "CALL STORED PROCEDURE"
        query = f"{query_type} {procedure_name} {procedure_arguments}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def drop_stored_procedure(self, procedure_name: str) -> None:
        query_type = "DROP STORED PROCEDURE"
        query = f"{query_type} {procedure_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def create_function(self, function_name: str, function_body: str) -> None:
        query_type = "FUNCTION"
        query = f"{query_type} {function_name} {function_body}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
    
    def drop_function(self, function_name: str) -> None:
        query_type = "DROP FUNCTION"
        query = f"{query_type} {function_name}"
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    # Would only need to sanatize input if user inputs table name or column name
    def __sanitize_input(self, input: str) -> str:
        # Remove any potentially dangerous characters
        sanitized_input = input.translate(str.maketrans('', '', '\'"<>;'))
        return sanitized_input

    # def __format_sql_query(self, query: str, params: tuple[str] | None = None) -> str:
    #     sql_query = query
    #     if params is not None:
    #         # Replace the ? placeholders with the query parameters
    #         sql_query = sql_query.replace("?", "{}")
    #         sql_query = sql_query.format(*params)
    #     return sql_query

    # def __handle_exists_result(self, result, item_name: str) -> bool:
    #     if result is not None:
    #         logging.debug(f"Table '{item_name}' exists.")
    #         return True
    #     else:
    #         logging.debug(f"Table '{item_name}' does not exist.")
    #         return False

    # def __item_exists(self, item_name: str, query: str, params: tuple | None = None) -> bool:
    #     # Format the SQL query
    #     sql_query = self.__format_sql_query(query, params)
    #     # Execute the query
    #     result = self.db_connection.execute_query(sql_query)
    #     # Handle the exists query result
    #     return self.__handle_exists_result(result, item_name)

    def __item_exists(self, item_name: str, query: str, params: tuple) -> bool:
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result is not None  # Returns True if a row is returned, indicating the item exists
        except Exception as e:
            raise DatabaseQueryError(self.db_connection, "Error executing query", e)

    def table_exists(self, table_name: str) -> bool:
        # SQL query to check if a table exists
        check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        # Set the query parameters
        params = (table_name,)
        # Check if the table exists
        return self.__item_exists(table_name, check_table_query, params)

    def column_exists(self, table_name: str, column_name: str) -> bool:
        # SQL query to check if a column exists
        check_column_query = f"SELECT count(*) FROM pragma_table_info('{table_name}') WHERE name='{column_name}'"
        # Set the query parameters
        params = (table_name, column_name)
        # Check if the column exists
        return self.__item_exists(column_name, check_column_query, params)

    def entry_exists(self, table_name: str, condition: str, user_id: int) -> bool:
        # Sanitize the input to avoid SQL injection
        table_name = self.__sanitize_input(table_name)
        condition = self.__sanitize_input(condition)

        # SQL query to check if the entry exists in the table
        check_entry_query = f"SELECT 1 FROM {table_name} WHERE {condition} AND user_id = ?"
        # Set the query parameters
        params = (user_id,)
        # Check if the entry exists
        return self.__item_exists(table_name, check_entry_query, params)










    def get_user_account_by_id(self, provided_user_id: int) -> UserAccount | None:
        # Define the query parameters
        query_type = "SELECT"
        get_user_account_by_id_query = f"{query_type} id, username FROM user WHERE id = ?"
        params = (str(provided_user_id),)
        # Execute the query
        result = self.execute_query(get_user_account_by_id_query, params)
        # Check whether the result is None (None means the user doesn't exist)
        if result is not None and len(result) > 0:
            return UserAccount(result[0][0], result[0][1])
        else:
            return None

    def get_user_account_by_username(self, provided_username: str) -> UserAccount | None:
        # Define the query parameters
        query_type = "SELECT"
        get_user_account_by_username_query = f"{query_type} id, username FROM user WHERE username = ?"
        params = (provided_username,)
        # Execute the query
        result = self.execute_query(get_user_account_by_username_query, params)
        # Check whether the result is None (None means the user doesn't exist)
        if result is not None and len(result) > 0:
            return UserAccount(result[0][0], result[0][1])
        else:
            return None

    def get_user_password_by_username(self, provided_username: str) -> bytes | None:
        # Define the query parameters
        query_type = "SELECT"
        get_user_account_by_username_query = f"{query_type} password_hash FROM user WHERE username = ?"
        params = (provided_username,)
        # Execute the query
        result = self.execute_query(get_user_account_by_username_query, params)
        # Check whether the result is None (None means the user doesn't exist)
        if result is not None and len(result) > 0:
            return result[0][0]
        else:
            return None







    def get_email_usage_name_by_usage_id(self, email_usage_id: int) -> str:
        # Define the query parameters
        query_type = "SELECT"
        get_email_usage_query = f"{query_type} usage FROM email_usage WHERE id = ?"
        params = (email_usage_id,)
        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_email_usage_query, params)
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def get_email_usage_id_by_usage_name(self, email_usage_name: str) -> int | None:
        # Define the query parameters
        query_type = "SELECT"
        get_email_usage_id_query = f"{query_type} id FROM email_usage WHERE usage = ?"
        params = (email_usage_name,)
        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_email_usage_id_query, params)
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def get_email_usage_by_email_address(self, provided_email_address: str) -> list[str] | None:
        # Define the query parameters
        query_type = "SELECT"
        get_email_account_by_email_address_query = f"{query_type} email_usage_id, [address] FROM email WHERE user_id = ? AND [address] = ?"
        params = (self.session_manager.get_current_user_id(), provided_email_address)
        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_email_account_by_email_address_query, params)
                result = cursor.fetchall()
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
        # Check if the user has any email accounts
        if result is None or len(result) > 0:
            return None
        # Initialize a list of EmailAccount types
        email_usage: list[str] = []
        # Replace the email usage id with the email usage name
        for row in result:
            usage = self.get_email_usage_name_by_usage_id(result[row][0])
            email_usage.append(usage)
            logging.debug(f"Email address: {provided_email_address}, usage: {usage}")
        return email_usage

    def get_all_user_email_accounts(self) -> list[EmailAccount] | None:
        # Define the query parameters
        query_type = "SELECT"
        get_email_accounts_query = f"{query_type} email_usage_id, [address] FROM email WHERE user_id = ?"
        params = (self.session_manager.get_current_user_id(),) # FIXME - no longer have access to current_user.user_id???
        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_email_accounts_query, params)
                result = cursor.fetchall()
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
        # Check if the user has any email accounts
        if result is None or len(result) > 0:
            return None
        # Initialize a list of EmailAccount types
        email_accounts: list[EmailAccount] = []
        # Replace the email usage id with the email usage name
        for row in result:
            usage = self.get_email_usage_name_by_usage_id(result[row][0])
            address = result[row][1]
            email_accounts.append(EmailAccount(usage, address))
            logging.debug(f"Email address: {address}, usage: {usage}")
        return email_accounts

    def get_user_email_accounts_by_usage(self, email_usage_name: str) -> list[EmailAccount] | None:
        # Define the query parameters
        query_type = "SELECT"
        get_email_accounts_query = f"{query_type} [address] FROM email WHERE user_id = ? AND email_usage_id = ?"
        params = (self.session_manager.get_current_user_id(), self.get_email_usage_id_by_usage_name(email_usage_name))
        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_email_accounts_query, params)
                result = cursor.fetchall()
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
        # Initialize a list of EmailAccount types
        email_accounts: list[EmailAccount] = []
        # Check if the user has any email accounts
        if result is not None:
            # Replace the email usage id with the email usage name
            for row in result:
                usage = email_usage_name
                address = row[0]
                email_accounts.append(EmailAccount(usage, address))
                logging.debug(f"Email address: {address}, usage: {usage}")
        return email_accounts

    # def get_email_password_hash(self, user_id: int, email_address: str) -> bytes | None:
    #     query_type = "SELECT"
    #     # SQL query to get the password for an email address
    #     get_email_password_query = f"{query_type} password FROM email WHERE user_id = ? AND email_address = ?"
    #     # Set the query parameters
    #     params = (user_id, email_address)

    #     # Execute the query
    #     try:
    #         with self.db_connection.cursor() as cursor:
    #             cursor.execute(get_email_password_query, params)
    #             result = cursor.fetchone()
    #             return result[0]
    #     except Exception as e:
    #         raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
        









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







    def handle_query_result(self, result, success_message: str, failure_message: str) -> list | None:
        if result is not None:
            print(success_message)
            return result
        else:
            print(failure_message)
            return None
        










    def table_is_empty(self, table_name: str) -> bool:
        query_type = "SELECT"
        # SQL query to check if a table is empty
        check_table_query = f"{query_type} * FROM ? LIMIT 1"
        # Set the query parameters
        params = (table_name,)

        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(check_table_query, params)
                result = cursor.fetchone()
                return result is None  # Returns True if no row is returned, indicating the table is empty
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)

    def store_username_and_password(self, username: str, password_hash: bytes) -> None:
        query_type = "INSERT"
        # SQL query to store the username and password hash
        store_username_and_password_query = f"{query_type} INTO user (username, password_hash) VALUES (?, ?)"
        # Set the query parameters
        params = (username, password_hash)

        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(store_username_and_password_query, params)
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)
     












    def get_data_type_id(self, user_id: int, data_type: str) -> int | None:
        query_type = "SELECT"
        # SQL query to get the id of a data type
        get_data_type_id_query = f"{query_type} id FROM data_type WHERE user_id = ? AND name = ?"
        # Set the query parameters
        params = (user_id, data_type)

        # Execute the query
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(get_data_type_id_query, params)
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            raise DatabaseQueryExecutionError(self.db_connection, query_type, e)


# DatabaseQueryError class  with Exception as base class for custom error handling
class DatabaseQueryError(Exception):
    def __init__(self, db_connection, message: str, original_exception=None) -> None:
        self.db_connection = str(db_connection).strip()
        self.message = message
        self.original_exception = str(original_exception).strip() if original_exception is not None else None

    def __str__(self) -> str:
        if self.original_exception is None:
            return f"Database query error: {self.message} on connection '{self.db_connection}'."
        return f"Database query error: {self.message} on connection '{self.db_connection}'.\
            \nOriginal exception: {self.original_exception}"


class DatabaseQueryExecutionError(Exception):
    def __init__(self, db_connection, query_type: str, original_exception=None) -> None:
        self.db_connection = str(db_connection).strip()
        self.query_type = query_type
        self.original_exception = str(original_exception).strip() if original_exception is not None else None

    def __str__(self) -> str:
        if self.original_exception is None:
            return f"[Database query error] Error executing {self.query_type} query on connection '{self.db_connection}'."
        return f"[Database query error] Error executing {self.query_type} query on connection '{self.db_connection}'.\
            \nOriginal exception: {self.original_exception}"

# try:
#     # Some code that may raise DatabaseConnectionError
# except DatabaseConnectionError as e:
#     print(f"Error occurred for database: {e.db_name}")
#     print(e)  # Prints the custom error message and database name


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
