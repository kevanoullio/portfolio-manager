# Purpose: Backup module for creating and restoring database backups.

# Standard Libraries
import shutil

# Third-party Libraries

# Local Modules
from data_management.database import DatabaseConnection
from data_management.schema import DatabaseSchema

# Configure logging
import logging


# BackupManager class for creating and restoring database backups
class BackupManager:
    def __init__(self, db_filename: str, db_schema_filename: str) -> None:
        self.db_filename: str = db_filename
        self.backup_filename: str = f"{self.db_filename}.bak"
        self.db_schema_filename: str = db_schema_filename
        self.db_connection = DatabaseConnection(self.db_filename)
        # self.db_schema = DatabaseSchema(self.db_connection)
        logging.info(f"Backup manager initialized. Database: {self.db_filename}")


    def restore_from_backup(self, destination_filename: str) -> bool:
        try:
            # Copy the backup file to the destination
            shutil.copyfile(self.backup_filename, destination_filename)
            return True
        except Exception as e:
            print(f"Failed to restore from backup: {str(e)}")
            return False


    def create_new_backup(self) -> bool:
        try:
            # Create a new backup database connection object
            backup_connection = DatabaseConnection(self.backup_filename)
            # Create a new backup database file by opening and closing a connection
            backup_connection.open_connection()
            # Create a new backup database schema object
            backup_database_schema = DatabaseSchema(backup_connection)
            # Initialize the backup database using the schema file
            backup_database_schema.initialize_database(self.db_schema_filename)
            # Close the backup database connection
            backup_connection.close_connection()
            logging.info("New backup database created and initialized successfully.")
            return True
        except Exception as e:
            logging.error(f"Failed to create a new backup database: {str(e)}")
            return False


    def setup_database_structure(self, db_connection: DatabaseConnection) -> None:
        try:
            # Create a new database schema object
            database_schema = DatabaseSchema(self.db_connection)
            # Initialize the database using the schema file
            database_schema.initialize_database(self.db_schema_filename)
            logging.info("Database structure initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialized the database structure: {str(e)}")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
