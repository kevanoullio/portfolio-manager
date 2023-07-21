# Purpose: Database Schema module for creating and initializing the database schema.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
from database_management.connection import DatabaseConnectionError

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from database_management.database import DatabaseConnection

# Configure logging
import logging


# DatabaseSchema class for creating and initializing the database schema
class DatabaseSchema:
    def __init__(self, db_connection: DatabaseConnection, db_schema_filename: str) -> None:
        self.db_connection = db_connection
        self.db_schema_filename = db_schema_filename

    def initialize_database(self) -> None:
        # TODO Check if initialization was successful, make sure the database file is deleted if it wasn't
        try:
            with self.db_connection as connection:
                with connection.cursor() as cursor:
                    # Read the schema file
                    with open(self.db_schema_filename, 'r') as database_schema_file:
                        schema_sql_script = database_schema_file.read()
                        # Execute the schema SQL statements
                        cursor.executescript(schema_sql_script)
                        logging.info("Database initialized using the Database schema.")
                        # Perform additional operations if needed
        except DatabaseConnectionError as e:
            logging.error(str(e))


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
