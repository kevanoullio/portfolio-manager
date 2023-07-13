# Purpose: DatabaseConnection class for opening and closing the database connection.

# Standard Libraries
from contextlib import contextmanager
import queue
import sqlite3

# Third-party Libraries

# Local Modules

# Configure logging
import logging
from config import configure_logging
configure_logging()


# DatabaseConnectionError class  with Exception as base class for custom error handling
class DatabaseConnectionError(Exception):
    def __init__(self, db_name: str, message: str, original_exception=None) -> None:
        self.db_name = db_name
        self.message = message
        self.original_exception = original_exception

    def __str__(self) -> str:
        if self.original_exception is None:
            return f"[{self.db_name}] {self.message}."
        return f"[{self.db_name}] {self.message}. {self.original_exception}"

# try:
#     # Some code that may raise DatabaseConnectionError
# except DatabaseConnectionError as e:
#     print(f"Error occurred for database: {e.db_name}")
#     print(e)  # Prints the custom error message and database name


# DatabaseConnection class for opening and closing the database connection
class DatabaseConnection:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self.connection = None
        logging.info(f"Database connection initialized. Database: {self.db_filename}")


    def __enter__(self):
        try:
            self.connection = self.open_connection()
        except Exception as e:
            self.close_connection()
            raise e
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()


    @contextmanager
    def cursor(self):
        if self.connection is not None:
            # connection = self.open_connection()
            cursor = self.connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()
        else:
            logging.error(f"Database connection is closed: {self.db_filename}")
            raise DatabaseConnectionError(self.db_filename, "Database connection is closed")


    def open_connection(self):
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(self.db_filename)
                return self.connection
            except sqlite3.Error as e:
                raise DatabaseConnectionError(self.db_filename, "Error opening the database connection", e)
        else:
            raise DatabaseConnectionError(self.db_filename, "Database connection is already open.")


    def close_connection(self):
        if self.connection is not None:
            try:
                self.connection.close()
                self.connection = None
            except sqlite3.Error as e:
                raise DatabaseConnectionError(self.db_filename, "Error closing the database connection", e)
        else:
            raise DatabaseConnectionError(self.db_filename, "Database connection is already closed")


    def begin_transaction(self):
        if self.connection is not None:
            self.connection.execute("BEGIN TRANSACTION")
        else:
            raise DatabaseConnectionError(self.db_filename, "Database connection is not open.")


    # def execute_query(self, sql_query: str) -> sqlite3.Cursor:
    #     if self.connection is not None:
    #         with self.cursor() as cursor:
    #             try:
    #                 result = cursor.execute(sql_query)
    #                 logging.debug(f"Query executed successfully: {sql_query}")
    #                 return result
    #             except sqlite3.Error as e:
    #                 raise DatabaseConnectionError(self.db_filename, "Error executing SQL query", e)
    #     else:
    #         raise DatabaseConnectionError(self.db_filename, "Database connection is closed")


    def commit_transaction(self):
            if self.connection is not None:
                try:
                    self.connection.commit()
                except sqlite3.Error as e:
                    raise DatabaseConnectionError(self.db_filename, "Error committing changes to the database", e)
            else:
                raise DatabaseConnectionError(self.db_filename, "Database connection is not open.")


    def rollback_transaction(self):
        if self.connection is not None:
            self.connection.rollback()
        else:
            raise DatabaseConnectionError(self.db_filename, "Database connection is not open.")


# # Open the database connection
# with DatabaseConnection("your_database.db") as connection:
#     # Begin a transaction
#     connection.begin_transaction()

#     try:
#         # Execute multiple queries within the transaction
#         connection.execute_query("INSERT INTO table1 (col1, col2) VALUES (1, 'A')")
#         connection.execute_query("UPDATE table2 SET col1 = 'B' WHERE col2 = 'X'")

#         # Commit the transaction
#         connection.commit_transaction()

#     except Exception:
#         # Rollback the transaction if an exception occurs
#         connection.rollback_transaction()






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


if __name__ == "__main__":
    pass
