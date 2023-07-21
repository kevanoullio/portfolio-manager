# Purpose: Main entry point for the portfolio manager application.

# Standard Libraries
import os

# Third-party Libraries

# Local Modules
from program_container.containers import MainContainer

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
    db_schema_filename = "./database_management/schema/schema.sql"

    # Create a container object
    main_container = MainContainer(db_filename, db_schema_filename)
    logging.debug("Program Container created.")

    # Start the database
    main_container.database.start()
    logging.debug("Database started.")

    # Run the dashboard
    main_container.dashboard.run()
    logging.debug("Dashboard started.")

    # Exit the program gracefully
    logging.info("Exiting the portfolio manager application.")
    exit(0)


if __name__ == "__main__":
    main()
