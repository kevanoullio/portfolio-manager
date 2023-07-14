# Purpose: Query Results module for handling and displaying the results of SQL queries.

# Standard Libraries

# Third-party Libraries

# Local Modules
from session.session_manager import SessionManager

# Configure logging
import logging



class QueryResults:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager


    def print(self, query_results) -> None:
        # Print the results in a table-like format
        for row in query_results:
            print(*row, sep="\t")


