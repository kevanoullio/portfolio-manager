# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import os

# Third-party Libraries

# Local Modules
from data_management.backup import BackupManager
from data_management.database import Database, DatabaseConnection, DatabaseSchema
from session.session_manager import SessionManager
from user_interface.dashboard import Dashboard

# Configure logging
import logging
from config import configure_logging


# Main entry point for the portfolio manager application
def main():
    configure_logging()
    logging.info("Starting the portfolio manager application.")

    # Create the data folder if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Set the database filenames
    db_filename = "./data/database.db"
    db_schema_filename = "./database/schema.sql"
    backup_manager = BackupManager(db_filename, db_schema_filename)
    backup_filename = backup_manager.backup_filename

    # Check if the database file exists
    if not os.path.exists(db_filename):
        # Handle the case when the database file does not exist
        logging.info("Database file does not exist.")

        # Check if a backup file exists
        if os.path.exists(backup_filename):
            # Restore from the backup file
            restore_success = backup_manager.restore_from_backup(db_filename)
            if restore_success:
                print("Restored from backup.")
                logging.info("Database file restored from backup successfully.")
                # Perform additional steps to restore the database state, if needed
            else:
                print("Failed to restore from backup.")
                logging.error("Failed to restore database file from backup.")
                # Handle the error or exit the program as necessary
        else:
            # Create a new database file by opening and closing a connection
            db_connection = DatabaseConnection(db_filename)
            db_connection.open_connection()
            # Initialize the database using the schema file
            db_schema = DatabaseSchema(db_connection)
            db_schema.initialize_database(db_schema_filename)
            # Close the database connection
            db_connection.close_connection()
            logging.info("Database file created and initialized successfully.")
    else:
        # Check if the backup file exists
        if not os.path.exists(backup_filename):
            # Handle the case when the backup file does not exist
            logging.info("Backup file does not exist.")
            # Create a new backup database file and initialize it
            backup_connection = backup_manager.create_new_backup()
            if backup_connection:
                print("Created a new backup database.")
            else:
                print("Failed to create a new database.")
                # Handle the error or exit the program as necessary


    # Create a database object
    database = Database(db_filename)
    # Open the database connection
    database.db_connection.open_connection()
    # Create the session manager
    session_manager = SessionManager(database)

    # Create a dashboard object
    dashboard = Dashboard(session_manager)
    # Run the dashboard
    dashboard.run()


    # Close the database connections
    database.db_connection.close_connection()
    logging.info(f"Database {db_filename} connection closed.")

    # Exit the program gracefully
    print("Exiting the program...")
    logging.info("Exiting the portfolio manager application.")

    exit(0)


if __name__ == "__main__":
    main()
