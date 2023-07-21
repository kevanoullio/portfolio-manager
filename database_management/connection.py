# Purpose: Database Connection module for managing the database connection.

# Standard Libraries
from contextlib import contextmanager
import queue
import sqlite3

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# DatabaseConnection class for managing the database connection
class DatabaseConnection:
    """The singleton pattern to ensure that there is only one instance of the DatabaseConnection classthroughout the application.
    \nThe key features of the Singleton pattern are:
    - Private Constructor: The Singleton class has a private constructor, meaning that it cannot be instantiated directly from outside the class.
    - Static Instance: The Singleton class maintains a static reference (often named _instance) to the single instance of the class that it creates.
    - Global Access: The Singleton provides a public static method (often named getInstance()) that allows clients to access the single instance of the class. This method ensures that only one instance is created and returned.
    """
    _instance = None

    def __new__(cls, db_filename: str):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._init_db(db_filename)
        return cls._instance

    def _init_db(self, db_filename: str):
        self.db_filename = db_filename
        self.connection = None
        logging.debug(f"Database connection initialized. Database: {self.db_filename}")

    def __enter__(self):
        """The __enter__ method is called when entering the context manager's scope.
        \nIt returns the context manager object itself.
        """
        try:
            self.open_connection()
        except Exception as e:
            self.close_connection()
            raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """The __exit__ method is called when exiting the context manager's scope.
        \nIf an exception is raised inside the 'with' block, the exception is passed to the __exit__ method.
        """
        self.close_connection()

    @contextmanager
    def cursor(self):
        if self.connection is not None:
            cursor = self.connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
        else:
            logging.error(f"Database connection is closed: {self.db_filename}")
            raise DatabaseConnectionError(self, "Database connection is closed")

    def open_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_filename)
            except sqlite3.Error as e:
                raise DatabaseConnectionError(self, "Error opening the database connection", e)
        else:
            raise DatabaseConnectionError(self, "Database connection is already open.")

    def close_connection(self) -> None:
        if self.connection is not None:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                raise DatabaseConnectionError(self, "Error closing the database connection", e)
        else:
            raise DatabaseConnectionError(self, "Database connection is already closed")

    def begin_transaction(self) -> None:
        if self.connection is not None:
            try:
                self.connection.execute("BEGIN TRANSACTION")
            except sqlite3.Error as e:
                raise DatabaseQueryExecutionError(self, "Error beginning a transaction", e)
        else:
            raise DatabaseConnectionError(self, "Database connection is not open.")

    def execute_query(self, sql_query: str, params: tuple | None=None) -> sqlite3.Cursor:
        """Executes an SQL query on the database and returns a cursor object.
        
        Can be used to execute a single query, or a sequence of queries separated by semicolons.

        Args:
            sql_query (str): The SQL query/ies to be executed.
            params (execute_query_params_type, optional): The parameters to use in the query/ies, if any. Defaults to None.

        Returns:
            (sqlite3.Cursor): A cursor object that can be used to iterate over the results of the query.

        Raises:
            DatabaseConnectionError: If the database connection is closed.
            DatabaseQueryExecutionError: If there is an error executing the query.

        Example usage:

            sql_query = '''

            INSERT INTO table1 (column1, column2) VALUES (?, ?);

            INSERT INTO table2 (column1, column2) VALUES (?, ?);

            '''

            params = (value1, value2, value3, value4)
            
            execute_query(sql_query, params)
        """
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                if params is not None:
                    result = cursor.execute(sql_query, params)
                else:
                    result = cursor.execute(sql_query)
                logging.debug(f"Query executed successfully: {sql_query}")
                return result
            except sqlite3.Error as e:
                raise DatabaseQueryExecutionError(self, "Error executing SQL query", e)
        else:
            raise DatabaseConnectionError(self, "Database connection is closed")

    def commit_transaction(self) -> None:
            if self.connection is not None:
                try:
                    self.connection.commit()
                except sqlite3.Error as e:
                    raise DatabaseQueryExecutionError(self, "Error committing changes to the database", e)
            else:
                raise DatabaseConnectionError(self, "Database connection is not open.")

    def rollback_transaction(self) -> None:
        if self.connection is not None:
            try:
                self.connection.rollback()
            except sqlite3.Error as e:
                raise DatabaseQueryExecutionError(self, "Error rolling back changes to the database", e)
        else:
            raise DatabaseConnectionError(self, "Database connection is not open.")


# # ConnectionPool class for managing a pool of database connections
# class ConnectionPool:
#     def __init__(self, db_filename, pool_size):
#         self.db_filename = db_filename
#         self.pool = queue.Queue(pool_size)
#         self._create_connections(pool_size)

#     def _create_connections(self, num_connections):
#         for _ in range(num_connections):
#             connection = sqlite3.connect(self.db_filename)
#             self.pool.put(connection)

#     def get_connection(self):
#         return self.pool.get()

#     def release_connection(self, connection):
#         self.pool.put(connection)

#     def close_all_connections(self):
#         while not self.pool.empty():
#             connection = self.pool.get()
#             connection.close()

# # Usage example
# pool = ConnectionPool("your_database.db", pool_size=10)

# # Get a connection from the pool
# connection = pool.get_connection()

# # Use the connection for database operations
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM your_table")
# results = cursor.fetchall()

# # Release the connection back to the pool
# pool.release_connection(connection)

# # Close all connections in the pool when no longer needed
# pool.close_all_connections()


# DatabaseConnectionError class with Exception as base class for custom error handling during database connection
class DatabaseConnectionError(Exception):
    def __init__(self, db_connection: DatabaseConnection, message: str, original_exception=None) -> None:
        self.db_connection = str(db_connection).strip()
        self.message = message
        self.original_exception = str(original_exception).strip() if original_exception is not None else None

    def __str__(self) -> str:
        if self.original_exception is None:
            return f"Database connection error: [{self.message}] on connection '{self.db_connection}'."
        return f"Database connection error: [{self.message}] on connection '{self.db_connection}'.\
            \nOriginal exception: {self.original_exception}"


# DatabaseQueryExecutionError class with Exception as base class for custom error handling during query execution
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


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
