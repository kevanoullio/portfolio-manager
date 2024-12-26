# Purpose: Database Queries class for executing SQL statements.

# Standard Libraries
import sqlite3

# Third-party Libraries
import pandas as pd

# Local Modules
from user_interface.user_input import UserInput
from account_management.accounts import UserAccount, EmailAccount
from database_management.connection import DatabaseConnection, DatabaseConnectionError
# from database_management.schema.asset_dataclass import AssetTransaction
from session_management.session_manager import SessionManager
from database_management.schema.asset_dataclass import AssetInfoWithIDs
from exceptions.database_exceptions import DatabaseQueryError, DatabaseQuerySyntaxError, DatabaseQueryExecutionError
from exceptions.authentication_exceptions import NoUserLoggedInError

# Configure logging
import logging


# QueryExecutor class for executing SQL statements
class QueryExecutor:
	def __init__(self, db_connection: DatabaseConnection, session_manager: SessionManager):
		self.__db_connection = db_connection
		self.__session_manager = session_manager
		self.__complex_queries_file = "./database_management/query/complex_queries.sql"
		logging.debug(f"Query executor initialized. Database: {self.__db_connection.db_filename}")

	def initialize_database_schema(self, db_schema_filename: str) -> None:
		try:
			with self.__db_connection as connection:
				try:
					with connection.cursor() as cursor:
						with open(db_schema_filename, "r") as database_schema_file:
							schema = database_schema_file.read()
							# Execute the schema SQL statements
							cursor.executescript(schema)
							logging.info("Database schema initialized using the schema.sql file.")
				except sqlite3.Error as e:
					logging.debug("Database schema initialization failed.")
					raise DatabaseQueryExecutionError(self.__db_connection, "Database schema initialization failed (sqlite3.Error)", None, None, e)
		except DatabaseConnectionError as e:
			logging.error("Database connection is closed.")
			raise DatabaseConnectionError(self.__db_connection, "Database connection is closed.")

	def dictionary_to_existing_sql_table(self, dictionary: dict, table_name: str) -> None:
		# Check if the dictionary is None or not
		if dictionary is not None:
			try:
				# Construct the INSERT statement
				columns = ", ".join(dictionary.keys())
				placeholders = ", ".join("?" * len(dictionary))
				query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
				# Execute the query
				self.execute_query(query, tuple(dictionary.values()))
				logging.info(f"Dictionary inserted into the '{table_name}' table.")
			except sqlite3.IntegrityError as e:
				logging.error(f"Dictionary could not be inserted into the '{table_name}' table. {e}")
		else:
			logging.error("Dictionary is None.")

	def dataframe_to_existing_sql_table(self, dataframe: pd.DataFrame, table_name: str) -> None:
		# Check if the dataframe is None or not
		if dataframe is not None:
			try:
				connection = sqlite3.connect(self.__db_connection.db_filename)
				try:
					# Insert all rows from the dataframe into the existing database table
					dataframe.to_sql(table_name, connection, index=False, if_exists="append")
					logging.info(f"Dataframe inserted into the '{table_name}' table.")
				except sqlite3.IntegrityError as e:
					logging.error(f"Dataframe could not be inserted into the '{table_name}' table. {e}")
			except sqlite3.Error as e:
				raise DatabaseConnectionError(self.__db_connection, "Error opening the database connection", e)
		else:
			logging.error("Dataframe is None.")

	def execute_query(self, query: str, params: tuple | None = None) -> list[tuple] | None:
		try:
			with self.__db_connection as connection:
				connection.begin_transaction()
				cursor = connection.execute_query(query, params)
				result = cursor.fetchall() # TODO - use QueryResults class to handle and format the results
				connection.commit_transaction()
				return result
		except sqlite3.OperationalError as e:
			logging.error(f"Query syntax error: {e}")
			raise DatabaseQuerySyntaxError(self.__db_connection, "qlite3.OperationalError", query, params, e)
		except sqlite3.DatabaseError as e:
			logging.error(f"Query execution error: {e}")
			raise DatabaseQueryExecutionError(self.__db_connection, "sqlite3.DatabaseError", query, params, e)
		except sqlite3.Error as e:
			logging.error(f"Error executing SQL query: {query}. {e}")
			raise DatabaseQueryError(self.__db_connection, "sqlite3.Error", query, params, e)
		except Exception as e:
			logging.error(f"Error executing SQL query: {query}. {e}")
			raise DatabaseQueryError(self.__db_connection, "Exception", query, params, e)

	def execute_query_sequence(self, queries: list[tuple[str, tuple]]) -> list[list[tuple]] | None:
		try:
			results = []
			with self.__db_connection as connection:
				connection.begin_transaction()
				for query, params in queries:
					cursor = connection.execute_query(query, params)
					results.append(cursor.fetchall())
				connection.commit_transaction()
			return results
		except sqlite3.OperationalError as e:
			logging.error(f"Query syntax error in sequence: {e}")
			raise DatabaseQuerySyntaxError(self.__db_connection, "(sqlite3.OperationalError) in sequence", None, None, e)
		except sqlite3.DatabaseError as e:
			logging.error(f"Query execution error in sequence: {e}")
			raise DatabaseQueryExecutionError(self.__db_connection, "(sqlite3.DatabaseError) in sequence", None, None, e)
		except sqlite3.Error as e:
			logging.error(f"Error executing SQL query sequence: {e}")
			raise DatabaseQueryError(self.__db_connection, "(sqlite3.Error) in sequence", None, None, e)
		except Exception as e:
			logging.error(f"Error executing SQL query sequence: {e}")
			raise DatabaseQueryError(self.__db_connection, "(sqlite3.Error) in sequence", None, None, e)

	def __find_complex_query_by_title(self, queries: str, query_title: str) -> str | None:
		individual_queries = queries.split(";")
		for i, query in enumerate(individual_queries):
			query = query.strip()
			query = query
			logging.debug(f"query: {query}")
			if query_title in query:
				logging.debug(f"Found query: {individual_queries[i].strip()}")
				return individual_queries[i].strip()
			# if query.startswith(" --"):
			#     comment = query[2:].strip()
			#     logging.debug(f"comment: {comment}")
			#     if query_title in comment:
			#         logging.debug(f"Found query: {individual_queries[i + 1].strip()}")
			#         return individual_queries[i + 1].strip()
		return None

	def __replace_variables(self, query: str, args) -> str:
		for arg in args:
			if isinstance(arg, str):
				# If the argument is a string, wrap it in single quotes
				query = query.replace('?', f"'{arg}'", 1)
			else:
				# If the argument is not a string, replace the placeholder without quotes
				query = query.replace('?', str(arg), 1)
		return query

	def execute_complex_query_by_title(self, query_title: str, *args: tuple) -> list[tuple] | None:
		# Read the complex_queries.sql file
		with open(self.__complex_queries_file, "r") as file:
			queries = file.read()

		# Find the selected query by matching the title
		selected_query = self.__find_complex_query_by_title(queries, query_title)

		# Check if the query was found
		if selected_query is None:
			raise DatabaseQueryError(self.__db_connection, f"Query with title '{query_title}' not found.")
		else:
			# Execute the selected query with variable substitution
			result = self.execute_query(self.__replace_variables(selected_query, args))
			return result


# Create Table: Creating a new table in the database.
# Drop Table: Removing an existing table from the database.
# Rename Table: Renaming an existing table in the database.
# Add Column: Adding a new column to an existing table.
# Alter Column: Modifying the properties or attributes of an existing column in a table.
# Drop Column: Removing a column from an existing table.
# Insert: Adding a new entry/row to a table.
# Update: Modifying existing entries/rows in a table.
# Delete: Removing entries/rows from a table.
# Select: Retrieving data from one or more tables.
# Join: Combining data from multiple tables based on a related column.
# Index: Creating an index on one or more columns to improve query performance.
# View: Virtual table that is based on the result of a SQL query.
# Trigger: Special type of stored procedure that is automatically executed when a certain event occurs, such as an insert, update, or delete operation.
# Constraint: Defining rules or conditions that the data must adhere to, such as primary keys, foreign keys, unique constraints, etc.
# Transaction: Grouping multiple queries into a single atomic unit of work that should either succeed or fail as a whole.
# Stored Procedure: Predefined set of SQL statements that can be executed as a single unit.

	# TODO - review all of this code and consolidate into query_builder
	def create_table(self, table_name: str, columns: tuple[str]) -> None:
		# Define the query parameters
		query_type = "CREATE TABLE"
		query = f"{query_type} IF NOT EXISTS {table_name} {columns}"
		# Execute the query
		self.execute_query(query)

	def rename_table(self, table_name: str, new_table_name: str) -> None:
		# Define the query parameters
		query_type = "ALTER TABLE"
		query = f"{query_type} {table_name} RENAME TO {new_table_name}"
		# Execute the query
		self.execute_query(query)

	def drop_table(self, table_name: str) -> None:
		# Define the query parameters
		query_type = "DROP TABLE"
		query = f"{query_type} IF EXISTS {table_name}"
		# Execute the query
		self.execute_query(query)

	def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
		# Define the query parameters
		query_type = "ADD COLUMN"
		query = f"ALTER TABLE {table_name} {query_type} {column_name} {data_type}"
		# Execute the query
		self.execute_query(query)

	def rename_column(self, table_name: str, column_name: str, new_column_name: str) -> None:
		# Define the query parameters
		query_type = "RENAME COLUMN"
		query = f"ALTER TABLE {table_name} {query_type} {column_name} TO {new_column_name}"
		# Execute the query
		self.execute_query(query)

	def alter_column(self, table_name: str, column_name: str, new_data_type: str) -> None:
		# Define the query parameters
		query_type = "ALTER COLUMN"
		query = f"ALTER TABLE {table_name} {query_type} {column_name} {new_data_type}"
		# Execute the query
		self.execute_query(query)

	def drop_column(self, table_name: str, column_name: str) -> None:
		# Define the query parameters
		query_type = "DROP COLUMN"
		query = f"ALTER TABLE {table_name} {query_type} {column_name}"
		# Execute the query

	def insert_entry(self, table_name: str, columns: tuple, values: tuple, user_id: int) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO {table_name} {columns} VALUES {values} WHERE user_id = {user_id}"
		# Execute the query
		self.execute_query(query)

	def update_entry(self, table_name: str, column_name: str, new_value: str, where_clause: str, user_id: int) -> None:
		# Define the query parameters
		query_type = "UPDATE"
		query = f"{query_type} {table_name} SET {column_name} = {new_value} WHERE {where_clause} AND user_id = {user_id}"
		# Execute the query
		self.execute_query(query)

	def delete_entry(self, table_name: str, columns: tuple, values: tuple, user_id: int) -> None:
		# Define the query parameters
		query_type = "DELETE"
		query = f"{query_type} FROM {table_name} WHERE {columns} = {values} AND user_id = {user_id}"
		# Execute the query
		self.execute_query(query)

	def select(self, table_name: str, columns: tuple[str], user_id: int, where_clause: str | None = None) -> list[tuple[str]] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} {columns} FROM {table_name}"
		if where_clause is not None:
			query += f" WHERE {where_clause} AND user_id = {user_id}"
		else:
			query += f" WHERE user_id = {user_id}"
		# Execute the query
		result = self.execute_query(query)
		# Check whether the result is None (None means ...) # TODO - what does None mean?
		if result is not None and len(result) > 0:
			return result
		else:
			return None

	def join(self, table_name_1: str, table_name_2: str, columns: tuple[str], join_condition: str, user_id: int) -> list[tuple[str]] | None:
		# Define the query parameters
		query_type = "JOIN"
		query = f"{query_type} {table_name_1} INNER JOIN {table_name_2} ON {join_condition} {columns} WHERE user_id = {user_id}"
		# Execute the query
		result = self.execute_query(query)
		# Check whether the result is None (None means ...) # TODO - what does None mean?
		if result is not None and len(result) > 0:
			return result
		else:
			return None

	def create_index(self, table_name: str, column_name: str) -> None:
		# Define the query parameters
		query_type = "CREATE INDEX"
		query = f"{query_type} ON {table_name} ({column_name})"
		# Execute the query
		self.execute_query(query)

	def drop_index(self, table_name: str, column_name: str) -> None:
		# Define the query parameters
		query_type = "DROP INDEX"
		query = f"{query_type} {table_name} {column_name}"
		# Execute the query
		self.execute_query(query)

	def create_view(self, view_name: str, view_body: str) -> None:
		# Define the query parameters
		query_type = "VIEW"
		query = f"{query_type} {view_name} {view_body}"
		# Execute the query
		self.execute_query(query)

	def drop_view(self, view_name: str) -> None:
		# Define the query parameters
		query_type = "DROP VIEW"
		query = f"{query_type} {view_name}"
		# Execute the query
		self.execute_query(query)

	def create_trigger(self, trigger_name: str, trigger_body: str) -> None:
		# Define the query parameters
		query_type = "TRIGGER"
		query = f"{query_type} {trigger_name} {trigger_body}"
		# Execute the query
		self.execute_query(query)

	def drop_trigger(self, trigger_name: str) -> None:
		# Define the query parameters
		query_type = "DROP TRIGGER"
		query = f"{query_type} {trigger_name}"
		# Execute the query
		self.execute_query(query)

	def create_constraint(self, table_name: str, constraint_type: str, column_name: str) -> None:
		# Define the query parameters
		query_type = "CREATE CONSTRAINT"
		query = f"{query_type} {constraint_type} {table_name} {column_name}"
		# Execute the query
		self.execute_query(query)

	def drop_constraint(self, table_name: str, constraint_type: str, column_name: str) -> None:
		# Define the query parameters
		query_type = "DROP CONSTRAINT"
		query = f"{query_type} {constraint_type} {table_name} {column_name}"
		# Execute the query
		self.execute_query(query)

	def create_transaction(self, queries: list[str]) -> None:
		# Define the query parameters
		query_type = "TRANSACTION"
		query = f"{query_type} {queries}"
		# Execute the query
		self.execute_query(query)

	def create_stored_procedure(self, procedure_name: str, procedure_body: str) -> None:
		# Define the query parameters
		query_type = "STORED PROCEDURE"
		query = f"{query_type} {procedure_name} {procedure_body}"
		# Execute the query
		self.execute_query(query)

	def call_stored_procedure(self, procedure_name: str, procedure_arguments: tuple[str]) -> None:
		# Define the query parameters
		query_type = "CALL STORED PROCEDURE"
		query = f"{query_type} {procedure_name} {procedure_arguments}"
		# Execute the query
		self.execute_query(query)

	def drop_stored_procedure(self, procedure_name: str) -> None:
		# Define the query parameters
		query_type = "DROP STORED PROCEDURE"
		query = f"{query_type} {procedure_name}"
		# Execute the query
		self.execute_query(query)

	def create_function(self, function_name: str, function_body: str) -> None:
		# Define the query parameters
		query_type = "FUNCTION"
		query = f"{query_type} {function_name} {function_body}"
		# Execute the query
		self.execute_query(query)

	def drop_function(self, function_name: str) -> None:
		# Define the query parameters
		query_type = "DROP FUNCTION"
		query = f"{query_type} {function_name}"
		# Execute the query
		self.execute_query(query)



	# def __format_sql_query(self, query: str, params: tuple[str] | None = None) -> str:
	#     sql_query = query
	#     if params is not None:
	#         # Replace the ? placeholders with the query parameters
	#         sql_query = sql_query.replace("?", "{}")
	#         sql_query = sql_query.format(*params)
	#     return sql_query

	# def __handle_exists_result(self, result, item_name: str) -> bool:
	#     if result is not None:
	#         logging.debug(f"Table '{item_name}' exists.")
	#         return True
	#     else:
	#         logging.debug(f"Table '{item_name}' does not exist.")
	#         return False

	# def __item_exists(self, item_name: str, query: str, params: tuple | None = None) -> bool:
	#     # Format the SQL query
	#     sql_query = self.__format_sql_query(query, params)
	#     # Execute the query
	#     result = self.db_connection.execute_query(sql_query)
	#     # Handle the exists query result
	#     return self.__handle_exists_result(result, item_name)

	def __item_exists(self, item_name: str, query: str, params: tuple) -> bool:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} {item_name} FROM {query}"
		# Execute the query
		result = self.execute_query(query, params)
		return result is not None  # Returns True if a row is returned, indicating the item exists

	def table_exists(self, table_name: str) -> bool:
		# Define the query parameters
		query_type = "SELECT"
		# SQL query to check if a table exists
		query = f"{query_type} name FROM sqlite_master WHERE type='table' AND name=?"
		# Set the query parameters
		params = (table_name,)
		# Check if the table exists
		return self.__item_exists(table_name, query, params)

	def column_exists(self, table_name: str, column_name: str) -> bool:
		# Define the query parameters
		query_type = "SELECT"
		# SQL query to check if a column exists
		query = f"{query_type} count(*) FROM pragma_table_info('{table_name}') WHERE name='{column_name}'"
		# Set the query parameters
		params = (table_name, column_name)
		# Check if the column exists
		return self.__item_exists(column_name, query, params)

	def entry_exists(self, table_name: str, condition: str, user_id: int) -> bool:
		# Sanitize the input to avoid SQL injection
		table_name = UserInput.sanitize_input(table_name)
		condition = UserInput.sanitize_input(condition)
		# Define the query parameters
		query_type = "SELECT"
		# SQL query to check if the entry exists in the table
		query = f"{query_type} 1 FROM {table_name} WHERE {condition} AND user_id = ?"
		# Set the query parameters
		params = (user_id,)
		# Check if the entry exists
		return self.__item_exists(table_name, query, params)

	def table_is_empty(self, table_name: str) -> bool:
		# Define the query parameters
		query_type = "SELECT"
		# SQL query to check if a table is empty
		query = f"{query_type} * FROM ? LIMIT 1"
		# Set the query parameters
		params = (table_name,)
		# Execute the query
		result = self.execute_query(query, params)
		return result is None  # Returns True if no row is returned, indicating the table is empty



	###########################
	# USER ACCOUNT OPERATIONS #
	###########################

	def store_username_and_password(self, username: str, password_hash: bytes) -> None:
		# Define the query parameters
		query_type = "INSERT"
		# SQL query to store the username and password hash
		query = f"{query_type} INTO user (user_role_id, username, password_hash) VALUES (?, ?, ?)"
		# Set the query parameters
		params = (2, username, password_hash)
		logging.debug(f"query: {query}")
		logging.debug(f"params: {params}")
		# Execute the query
		self.execute_query(query, params)

	def get_user_account_by_id(self, provided_user_id: int) -> UserAccount | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id, username FROM user WHERE id = ?"
		params = (str(provided_user_id),)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the user doesn't exist)
		if result is not None and len(result) > 0:
			return UserAccount(result[0][0], result[0][1])
		else:
			return None

	def get_user_account_by_username(self, provided_username: str) -> UserAccount | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id, username FROM user WHERE username = ?"
		params = (provided_username,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the user doesn't exist)
		if result is not None and len(result) > 0:
			return UserAccount(result[0][0], result[0][1])
		else:
			return None

	def get_user_password_by_username(self, provided_username: str) -> bytes | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} password_hash FROM user WHERE username = ?"
		params = (provided_username,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the user doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None


	############################
	# EMAIL ACCOUNT OPERATIONS #
	############################

	def store_email_address_only(self, email_usage_id: int, email_address: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO email (user_id, email_usage_id, [address]) VALUES (?, ?, ?)"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			params = (current_user_id, email_usage_id, email_address)
			# Execute the query
			self.execute_query(query, params)

	def store_email_address_and_password_hash(self, email_usage_id: int, email_address: str, email_password_hash: bytes) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO email (user_id, email_usage_id, [address], password_hash) VALUES (?, ?, ?, ?)"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			params = (current_user_id, email_usage_id, email_address, email_password_hash)
		# Execute the query
		self.execute_query(query, params)

	def get_email_usage_name_by_usage_id(self, email_usage_id: int) -> str | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} usage FROM email_usage WHERE id = ?"
		params = (email_usage_id,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the email_usage doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_email_usage_id_by_email_usage_name(self, email_usage_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM email_usage WHERE usage = ?"
		params = (email_usage_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the email_usage_id doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_email_usage_names_by_email_address(self, provided_email_address: str) -> list[str] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} email_usage_id, [address] FROM email WHERE user_id = ? AND [address] = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			params = (current_user_id, provided_email_address)
			# Execute the query
			result = self.execute_query(query, params)
			# Check if the user has any email accounts
			if result is None or len(result) > 0:
				return None
			# Initialize a list of EmailAccount types
			email_usage: list[str] = []
			# Replace the email usage id with the email usage name
			for row in result:
				usage = self.get_email_usage_name_by_usage_id(int(row[0]))
				if usage is not None:
					email_usage.append(usage)
					logging.debug(f"Email address: {provided_email_address}, usage: {usage}")
			return email_usage

	def get_all_current_user_email_accounts(self) -> list[EmailAccount] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} email_usage_id, [address] FROM email WHERE user_id = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			params = (current_user_id,)
			# Execute the query
			result = self.execute_query(query, params)
			logging.debug(f"result: {result}")
			# Check if the user has any email accounts
			if result is None or len(result) <= 0:
				return None
			# Use a list comprehension to create a list of EmailAccount types
			email_accounts = [
				EmailAccount(
					str(self.get_email_usage_name_by_usage_id(tuple[0])),
					str(tuple[1])
				)
				for tuple in result
			]
			# Log debug messages for each email account
			for email_account in email_accounts:
				logging.debug(f"Email address: {email_account.address}, usage: {email_account.usage}")
			return email_accounts

	def get_user_email_accounts_by_usage(self, email_usage_name: str) -> list[EmailAccount] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} [address] FROM email WHERE user_id = ? AND email_usage_id = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			email_usage_id = self.get_email_usage_id_by_email_usage_name(email_usage_name)
			if email_usage_id is None:
				raise DatabaseQueryError(self.__db_connection, f"Email usage '{email_usage_name}' does not exist.")
			else:
				params = (current_user_id, str(email_usage_id))
				# Execute the query
				result = self.execute_query(query, params)
				# Check if the user has any email accounts
				if result is None:
					return None
				# Initialize a list of EmailAccount types
				email_accounts: list[EmailAccount] = []
				# Replace the email usage id with the email usage name
				for row in result:
					usage = email_usage_name
					address = row[0]
					email_accounts.append(EmailAccount(usage, address))
					logging.debug(f"Email address: {address}, usage: {usage}")
				return email_accounts

	def get_email_account_by_email_address(self, email_address: str) -> EmailAccount | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} email_usage_id, address FROM email WHERE user_id = ? AND address = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")

		# Check if the user is logged in
		if current_user_id is None:
			raise NoUserLoggedInError(None)

		# Set the query parameters
		params = (current_user_id, email_address)
		# Execute the query
		result = self.execute_query(query, params)
		logging.debug(f"result: {result}")

		# Check if the user has any email accounts
		if result is None or len(result) <= 0:
			return None

		# Replace the email usage id with the email usage name
		usage: str | None = self.get_email_usage_name_by_usage_id(int(result[0][0]))
		if usage is None:
			raise DatabaseQueryError(self.__db_connection, f"Email usage id '{result[0][0]}' does not exist.")

		return EmailAccount(usage, email_address)

	def get_email_account_password_hash_by_email_address(self, email_address: str) -> bytes | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} password_hash FROM email WHERE user_id = ? AND address = ?"

		# Get the current user id
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")

		# Check if the user is logged in
		if current_user_id is None:
			raise NoUserLoggedInError(None)

		# Set the query parameters
		params = (current_user_id, email_address)
		# Execute the query
		result = self.execute_query(query, params)

		return result[0][0] if result is not None else None


	###############
	# MARKET DATA #
	###############

	def get_country_id_by_country_iso_code(self, country_iso_code: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM country WHERE iso_code = ?"
		params = (country_iso_code,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the country doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_city_id_by_city_name(self, city_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM city WHERE name = ?"
		params = (city_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the city doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_exchange_id_by_exchange_acronym(self, exchange_acronym: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM exchange WHERE acronym = ?"
		params = (exchange_acronym,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the exchange doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def insert_city(self, city_name: str, country_name: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO city (name, country_id) VALUES (?, ?)"
		country_id = self.get_country_id_by_country_name(country_name)
		params = (city_name, country_id)
		# Execute the query
		self.execute_query(query, params)

	def insert_exchange(self, country_id: int, exchange_name: str, exchange_acronym: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO exchange (country_id, name, acronym) VALUES (?, ?, ?)"
		params = (country_id, exchange_name, exchange_acronym)
		# Execute the query
		self.execute_query(query, params)

	def get_exchange_listing_symbols_by_exchange_acronym(self, exchange_acronym: str) -> list[str] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} symbol FROM exchange_listing WHERE exchange_id = (SELECT id FROM exchange WHERE acronym = ?)"
		params = (exchange_acronym,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the exchange doesn't exist)
		if result is not None and len(result) > 0:
			return [row[0] for row in result]
		else:
			return None


	##############
	# ASSET INFO #
	##############

	def get_all_asset_class_names(self) -> list[str] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} name FROM asset_class"
		# Execute the query
		result = self.execute_query(query)
		# Check whether the result is None (None means the asset class doesn't exist)
		if result is not None and len(result) > 0:
			return [row[0] for row in result]
		else:
			return None

	def get_asset_class_id_by_asset_class_name(self, asset_class_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM asset_class WHERE name = ?"
		params = (asset_class_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the asset class doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_all_asset_subclass_names(self) -> list[str] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} name FROM asset_subclass"
		# Execute the query
		result = self.execute_query(query)
		# Check whether the result is None (None means the asset subclass doesn't exist)
		if result is not None and len(result) > 0:
			return [row[0] for row in result]
		else:
			return None

	def get_asset_subclass_id_by_asset_subclass_name(self, asset_subclass_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM asset_subclass WHERE name = ?"
		params = (asset_subclass_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the asset subclass doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_asset_subclass_names_by_asset_class_name(self, asset_class_name: str) -> list[str] | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} asset_subclass.name FROM asset_subclass JOIN asset_class ON asset_subclass.asset_class_id = asset_class.id WHERE asset_class.name = ?"
		params = (asset_class_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the asset subclass doesn't exist)
		if result is not None and len(result) > 0:
			return [row[0] for row in result]
		else:
			return None

	def get_sector_id_by_sector_name(self, sector_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM sector WHERE name = ?"
		params = (sector_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the sector doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def insert_sector(self, asset_class_id: int, sector_name: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO sector (asset_class_id, name) VALUES (?, ?)"
		params = (asset_class_id, sector_name)
		# Execute the query
		self.execute_query(query, params)

	def get_industry_id_by_industry_name(self, industry_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM industry WHERE name = ?"
		params = (industry_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the industry doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def insert_industry(self, sector_id: int, industry_name: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO industry (sector_id, name) VALUES (?, ?)"
		params = (sector_id, industry_name)
		# Execute the query
		self.execute_query(query, params)

	def get_country_id_by_country_name(self, country_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM country WHERE name = ?"
		params = (country_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the country doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_country_id_by_exchange_id(self, exchange_id: int) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} country_id FROM exchange WHERE id = ?"
		params = (exchange_id,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the country doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_currency_id_by_currency_iso_code(self, currency_iso_code: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM currency WHERE iso_code = ?"
		params = (currency_iso_code,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the currency doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_currency_iso_code_by_currency_id(self, currency_id: int) -> str | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} iso_code FROM currency WHERE id = ?"
		params = (currency_id,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the currency doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_security_name_by_exchange_id_and_symbol(self, exchange_id: int, asset_symbol: str) -> str | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} security_name FROM exchange_listing WHERE exchange_id = ? AND symbol = ?"
		params = (exchange_id, asset_symbol)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the company doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def insert_asset_info_with_ids(self, asset_info_with_ids: AssetInfoWithIDs) -> None:
		# Define the query parameters
		query = "SELECT"
		# Check if a row with the same exchange_id and symbol already exists
		query = f"{query} * FROM asset_info WHERE exchange_id = ? AND symbol = ?"
		result = self.execute_query(query, (asset_info_with_ids.exchange_id, asset_info_with_ids.symbol))
		if result:
			print(f"A row with exchange_id {asset_info_with_ids.exchange_id} and symbol {asset_info_with_ids.symbol} already exists in the asset_info table.")
			logging.info(f"A row with exchange_id {asset_info_with_ids.exchange_id} and symbol {asset_info_with_ids.symbol} already exists in the asset_info table.")
			return None

		# Define the query parameters
		query = "INSERT"
		insert_asset_info_query = f"{query} INTO asset_info (asset_class_id, asset_subclass_id, " \
			f"sector_id, industry_id, country_id, city_id, financial_currency_id, exchange_currency_id, " \
			f"exchange_id, symbol, security_name, business_summary, website, logo_url) "\
			f"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
		# Define the query parameters
		params = (asset_info_with_ids.asset_class_id, asset_info_with_ids.asset_subclass_id, asset_info_with_ids.sector_id,
			asset_info_with_ids.industry_id, asset_info_with_ids.country_id, asset_info_with_ids.city_id, asset_info_with_ids.financial_currency_id,
			asset_info_with_ids.exchange_currency_id, asset_info_with_ids.exchange_id, asset_info_with_ids.symbol, asset_info_with_ids.security_name,
			asset_info_with_ids.business_summary, asset_info_with_ids.website, asset_info_with_ids.logo_url)
		# Execute the query
		self.execute_query(insert_asset_info_query, params)
		print(f"{asset_info_with_ids.symbol} successfully inserted into database for exchange_id {asset_info_with_ids.exchange_id}.")
		logging.info(f"{asset_info_with_ids.symbol} successfully inserted into database for exchange_id {asset_info_with_ids.exchange_id}.")




	######################
	# ASSET TRANSACTIONS #
	######################

	def get_last_uid_by_email_address_and_folder_name(self, email_address: str, folder_name: str) -> int | None:
		# Define the first query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM email WHERE user_id = ? AND email_usage_id = ? AND address = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			# Get the email_usage_id
			email_usage_id = self.get_email_usage_id_by_email_usage_name("import")
			if email_usage_id is None:
				return None

			# Execute the query
			result = self.execute_query(query, (current_user_id, email_usage_id, email_address))
			# Check whether the result is None (None means the email doesn't exist)
			if result is None or len(result) == 0:
				return None
			else:
				email_id = result[0][0]
				# Define the second query parameters
				query = f"{query_type} last_uid FROM imported_email_log WHERE user_id = ? \
					AND email_id = ? AND folder_name = ? ORDER BY last_uid DESC LIMIT 1;"
				params = (current_user_id, email_id, folder_name)
				# Execute the query
				result = self.execute_query(query, params)
				# Check whether the result is None (None means the email doesn't exist)
				if result is not None and len(result) > 0:
					return result[0][0]
				else:
					return None

	def insert_uid_by_email_address_and_folder_name(self, email_address: str, folder_name: str, last_uid: int) -> None:
		# Define the first query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM email WHERE user_id = ? AND address = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			# Execute the query
			result = self.execute_query(query, (current_user_id, email_address))
			# Check whether the result is None (None means the email doesn't exist)
			if result is None or len(result) == 0:
				return None
			else:
				email_id = result[0][0]
				# Define the second query parameters
				query_type = "INSERT"
				query = f"{query_type} INTO imported_email_log (user_id, email_id, folder_name, last_uid) VALUES (?, ?, ?, ?)"
				params = (current_user_id, email_id, folder_name, last_uid)
				# Execute the query
				self.execute_query(query, params)

	def get_asset_id_by_asset_symbol(self, asset_symbol: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM asset WHERE symbol = ?"
		params = (asset_symbol,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the asset doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_transaction_type_id_by_transaction_type_name(self, transaction_type_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM transaction_type WHERE name = ?"
		params = (transaction_type_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the transaction type doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def get_brokerage_id_by_brokerage_name(self, brokerage_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM brokerage WHERE name = ?"
		params = (brokerage_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the brokerage doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	def insert_brokerage(self, brokerage_name: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO brokerage (user_id, name) VALUES (?, ?)"
		current_user_id = self.__session_manager.get_current_user_id()
		logging.debug(f"Current user id: {current_user_id}")
		if current_user_id is None:
			raise NoUserLoggedInError(None)
		else:
			params = (current_user_id, brokerage_name)
			# Execute the query
			self.execute_query(query, params)

	def insert_investment_account(self, brokerage_id: int, investment_account_name: str) -> None:
		# Define the query parameters
		query_type = "INSERT"
		query = f"{query_type} INTO investment_account (user_id, brokerage_id, name) VALUES (?, ?, ?)"
		current_user_id = self.__session_manager.get_current_user_id()
		params = (current_user_id, brokerage_id, investment_account_name)
		# Execute the query
		self.execute_query(query, params)

	def get_investment_account_id_by_investment_account_name(self, brokerage_id: int, investment_account_name: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		query = f"{query_type} id FROM investment_account WHERE user_id = ? AND brokerage_id = ? AND name = ?"
		current_user_id = self.__session_manager.get_current_user_id()
		params = (current_user_id, brokerage_id, investment_account_name,)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the investment account doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None

	# def insert_asset_transaction(self, asset_transaction: AssetTransaction) -> None:
	#     # Define the query parameters
	#     query_type = "INSERT"
	#     query = f"{query_type} INTO asset_transaction (user_id, asset_id, transaction_type_id, " \
	#         f"brokerage_id, investment_account_id, quantity, avg_price, total, transaction_fee, transaction_date, " \
	#         f"imported_from, import_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
	#     current_user_id = self.__session_manager.get_current_user_id()
	#     params = (current_user_id, asset_transaction.asset_id, asset_transaction.transaction_type_id,
	#         asset_transaction.brokerage_id, asset_transaction.investment_account_id, asset_transaction.quantity,
	#         asset_transaction.avg_price, asset_transaction.total, asset_transaction.transaction_fee,
	#         asset_transaction.transaction_date, asset_transaction.imported_from, asset_transaction.import_date)
	#     # Execute the query
	#     result = self.execute_query(query, params)
	#     # Check whether the result is None (None means the asset transaction wasn't inserted)
	#     if result is not None and len(result) > 0:
	#         print(f"Asset transaction for {asset_transaction.asset_id} successfully inserted into database.")
	#         logging.info(f"Asset transaction for {asset_transaction.asset_id} successfully inserted into database.")
	#     else:
	#         print(f"Asset transaction for {asset_transaction.asset_id} was not inserted into database.")
	#         logging.info(f"Asset transaction for {asset_transaction.asset_id} was not inserted into database.")









	def __get_allowable_table_names(self) -> list[str]:
		allowable_table_names = []

		with open("./database/schema.sql", "r") as file:
			schema = file.read()
			# Split the schema into lines
			lines = schema.split("\n")

			# Iterate over the lines
			for line in lines:
				line = line.strip()

				# Check if the line starts with "CREATE TABLE IF NOT EXISTS"
				if line.startswith("CREATE TABLE IF NOT EXISTS"):
					# Extract the table name from the line
					table_name = line.split()[5].strip("`")
					allowable_table_names.append(table_name)

		return allowable_table_names







	def handle_query_result(self, result, success_message: str, failure_message: str) -> list | None:
		if result is not None:
			print(success_message)
			return result
		else:
			print(failure_message)
			return None












	def get_data_type_id(self, user_id: int, data_type: str) -> int | None:
		# Define the query parameters
		query_type = "SELECT"
		# SQL query to get the id of a data type
		query = f"{query_type} id FROM data_type WHERE user_id = ? AND name = ?"
		# Set the query parameters
		params = (str(user_id), data_type)
		# Execute the query
		result = self.execute_query(query, params)
		# Check whether the result is None (None means the data type doesn't exist)
		if result is not None and len(result) > 0:
			return result[0][0]
		else:
			return None






# try:
#     # Some code that may raise DatabaseConnectionError
# except DatabaseConnectionError as e:
#     print(f"Error occurred for database: {e.db_name}")
#     print(e)  # Prints the custom error message and database name


if __name__ == "__main__":
	print("This module is not meant to be executed directly.")
