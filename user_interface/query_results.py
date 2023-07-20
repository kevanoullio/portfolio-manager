# Purpose: Query Results module for handling and displaying the results of SQL queries.

# Standard Libraries

# Third-party Libraries

# Local Modules
from account_management.accounts import UserAccount, EmailAccount
from account_management.account_operations import UserAccountOperation, EmailAccountOperation

# Configure logging
import logging


# QueryResults class for handling and displaying the results of SQL queries
class QueryResults:
    def __init__(self) -> None:
        pass

    def print(self, query_results) -> None:
        # Print the results in a table-like format
        for row in query_results:
            print(*row, sep="\t")


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
