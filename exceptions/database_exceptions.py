# Purpose: Define custom exceptions for database errors.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries

# Third-party Libraries

# Local Modules
if TYPE_CHECKING:
	from database_management.connection import DatabaseConnection

# Configure logging


# Custom Exception for database errors
class DatabaseError(Exception):
	"""Base class for database exceptions."""
	def __init__(self, db_connection: DatabaseConnection, message: str, query: str | None = None, params: tuple | None = None, original_exception: Exception | None = None) -> None:
		self.db_connection = str(db_connection).strip()
		self.message = message
		self.query = query
		self.params = params
		self.original_exception = str(original_exception).strip() if original_exception is not None else None
		super().__init__(self.message)

	def __str__(self) -> str:
		error_output = f"{self.__class__.__name__}: {self.message} on connection '{self.db_connection}'."
		if self.query:
			error_output += f"\nQuery: {self.query}"
		if self.params:
			error_output += f"\nParams: {self.params}"
		if self.original_exception:
			error_output += f"\nOriginal exception: {self.original_exception}"
		return error_output

# DatabaseConnectionError class with DatabaseError(Exception) as base class for custom error handling during database connection
class DatabaseConnectionError(DatabaseError):
	def __init__(self, db_connection: DatabaseConnection, message: str, original_exception: Exception | None = None) -> None:
		super().__init__(db_connection, message, None, None, original_exception)

class DatabaseQuerySyntaxError(DatabaseError):
	def __init__(self, db_connection: DatabaseConnection, message: str, query: str | None = None, params: tuple | None = None, original_exception: Exception | None = None) -> None:
		base_message: str = f"Syntax error in SQL query statement"
		if message:
			base_message += f": {message}"
		super().__init__(db_connection, base_message, query, params, original_exception)

# DatabaseQueryExecutionError class with DatabaseError(Exception) as base class for custom error handling
class DatabaseQueryExecutionError(DatabaseError):
	def __init__(self, db_connection: DatabaseConnection, message: str, query: str | None = None, params: tuple | None = None, original_exception: Exception | None = None) -> None:
		base_message: str = f"Error executing SQL query statement due to syntax error"
		if message:
			base_message += f": {message}"
		super().__init__(db_connection, base_message, query, params, original_exception)

# DatabaseQueryOperationError class with DatabaseError(Exception) as base class for custom error handling
class DatabaseQueryOperationError(DatabaseError):
	"""Exception for errors in a sequence of query operations."""
	def __init__(self, db_connection: DatabaseConnection, message: str, queries: list[tuple[str, tuple]] | None, original_exception: Exception | None = None) -> None:
		base_message: str = f"Error executing sequence of SQL query operations"
		if message:
			base_message += f": {message}"

		# Extract query and params from queries list
		query = ""
		params_list = []
		if queries:
			for query_tuple in queries:
				query += f"\nQuery: {query_tuple[0]}"
				params_list.append(query_tuple[1])
			params = tuple(params_list)
		else:
			query = None
			params = None

		super().__init__(db_connection, base_message, query, params, original_exception)

# DatabaseQueryError class with DatabaseError(Exception) as base class for custom error handling
class DatabaseQueryError(DatabaseError):
	"""Exception for database query errors."""
	def __init__(self, db_connection: DatabaseConnection, message: str, query: str | None = None, params: tuple | None = None, original_exception: Exception | None = None) -> None:
		base_message: str = f"Error executing SQL query"
		if message:
			base_message += f": {message}"
		super().__init__(db_connection, base_message, query, params, original_exception)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
