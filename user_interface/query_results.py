# Purpose: Query Results module for handling and displaying the results of SQL queries.

# Standard Libraries

# Third-party Libraries

# Local Modules
from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# QueryResults class for handling and displaying the results of SQL queries
class QueryResults:
    def __init__(self) -> None:
        pass

    def simple_row_print(self, query_results, currency: bool = False) -> None:
        # Print the results in a table-like format
        if currency:
            # Find the maximum length of the float values
            max_length = max(len(f"{value:.2f}") for row in query_results for value in row if isinstance(value, float))

            for row in query_results:
                formatted_row = [f"${value:.2f}".rjust(max_length + 1) if isinstance(value, float) else value for value in row]
                print("\t".join(str(item) for item in formatted_row))
        else:
            for row in query_results:
                print("\t".join(str(item) for item in row))
    
    def print_rows_with_headers(self, headers: list[str], query_results, currency: bool = False) -> None:
        # Combine headers and query_results for alignment calculation
        combined = [headers] + query_results

        # Find the maximum length of each column
        column_lengths = [max(len(f"${value:.2f}") if isinstance(value, float) else len(str(value)) for value in column) for column in zip(*combined)]

        # Print the headers
        formatted_headers = [header.ljust(length) for header, length in zip(headers, column_lengths)]
        print("\t".join(formatted_headers))

        if currency:
            for row in query_results:
                formatted_row = [f"${value:.2f}".ljust(length) if isinstance(value, float) else str(value).ljust(length) for value, length in zip(row, column_lengths)]
                print("\t".join(formatted_row))
        else:
            for row in query_results:
                formatted_row = [str(value).ljust(length) for value, length in zip(row, column_lengths)]
                print("\t".join(formatted_row))


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
