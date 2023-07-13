# Purpose: Database Schema module for creating and initializing the database schema.

# Standard Libraries

# Third-party Libraries

# Local Modules
from data_management.connection import DatabaseConnection

# Configure logging
import logging
from config import configure_logging
configure_logging()


# DatabaseSchema class for creating and initializing the database schema
class DatabaseSchema:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection


    def initialize_database(self, schema_filename):
        # TODO Check if initialization was successful, make sure the database file is deleted if it wasn't
        with self.db_connection.cursor() as cursor:
            # Read the schema file
            with open(schema_filename, 'r') as schema_file:
                schema_sql = schema_file.read()

                # Execute the schema SQL statements
                cursor.executescript(schema_sql)

                logging.info("Database initialized using the Database schema.")
                # Perform additional operations if needed


if __name__ == "__main__":
    pass
