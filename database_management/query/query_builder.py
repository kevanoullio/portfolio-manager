# Purpose: Query Builder module for building complex queries based on user input or other criteria.

# Standard Libraries

# Third-party Libraries

# Local Modules
from account_management.accounts import UserAccount, EmailAccount
from database_management.query.query_executor import QueryExecutor

# Configure logging
import logging


# QueryBuilder class for building complex queries based on user input or other criteria
class QueryBuilder:
    def __init__(self, table):
        self.table = table
        self.columns = '*'
        self.where_clauses = []
        self.join_clauses = []

    def select(self, columns):
        self.columns = ', '.join(columns)
        return self
    
    ''' Example usage:
    query = QueryBuilder('users').select(['id', 'name', 'email']).where('age', '>', 18).build()
    print(query)  # SELECT id, name, email FROM users WHERE age > '18'
    '''
    def where(self, column, operator, value):
        self.where_clauses.append(f"{column} {operator} '{value}'")
        return self
    
    def insert_entry(self, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f"'{v}'" for v in data.values()])
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({values})"
        return query

    def update_entry(self, data):
        set_clause = ', '.join([f"{k} = '{v}'" for k, v in data.items()])
        query = f"UPDATE {self.table} SET {set_clause}"
        if self.where_clauses:
            where_clause = ' AND '.join(self.where_clauses)
            query += f" WHERE {where_clause}"
        return query
    
    def delete_entry(self):
        query = f"DELETE FROM {self.table}"
        if self.where_clauses:
            where_clause = ' AND '.join(self.where_clauses)
            query += f" WHERE {where_clause}"
        return query

    def create_table(self, columns):
        columns_clause = ', '.join(columns)
        query = f"CREATE TABLE {self.table} ({columns_clause})"
        return query

    def alter_table(self, alter_statement):
        query = f"ALTER TABLE {self.table} {alter_statement}"
        return query

    def rename_table(self, new_name):
        query = f"ALTER TABLE {self.table} RENAME TO {new_name}"
        return query

    def drop_table(self):
        query = f"DROP TABLE {self.table}"
        return query

    def add_column(self, column):
        query = f"ALTER TABLE {self.table} ADD COLUMN {column}"
        return query

    # # SQLite doesn’t support removing or renaming or altering columns in any way directly, but you can achieve the same result by
    # # creating a new table without the column you want to remove, copying the data from the
    # # old table to the new table, and then dropping the old table.
    # def remove_column(self, column):
    #     # Get the list of columns in the table
    #     # TODO - looks like this should not go in the query_builder if it needs a connection and is so complex?
    #     cursor = self.connection.execute(f'PRAGMA table_info({self.table})')
    #     columns = [row[1] for row in cursor.fetchall() if row[1] != column]
    #     columns_clause = ', '.join(columns)

    #     # Generate the SQL statements to remove the column
    #     queries = [
    #         f'BEGIN TRANSACTION',
    #         f'CREATE TEMPORARY TABLE {self.table}_backup({columns_clause})',
    #         f'INSERT INTO {self.table}_backup SELECT {columns_clause} FROM {self.table}',
    #         f'DROP TABLE {self.table}',
    #         f'CREATE TABLE {self.table}({columns_clause})',
    #         f'INSERT INTO {self.table} SELECT {columns_clause} FROM {self.table}_backup',
    #         f'DROP TABLE {self.table}_backup',
    #         f'COMMIT'
    #     ]
    #     return queries

    def group_by(self, columns):
        self.group_by_clause = ', '.join(columns)
        return self
    
    def join(self, table, join_type, condition):
        self.join_clauses.append(f"{join_type} JOIN {table} ON {condition}")
        return self

    def create_index(self, index_name, column, options=''):
        query = f"CREATE INDEX {options} {index_name} ON {self.table} ({column})"
        return query

    def drop_index(self, index_name):
        query = f"DROP INDEX {index_name}"
        return query

    def create_view(self, view_name, select_statement, options=''):
        query = f"CREATE VIEW {options} {view_name} AS {select_statement}"
        return query

    def drop_view(self, view_name):
        query = f"DROP VIEW {view_name}"
        return query


    def build(self):
        query = f"SELECT {self.columns} FROM {self.table}"
        if hasattr(self, 'join_clauses'):
            join_clause = ' '.join(self.join_clauses)
            query += f" {join_clause}"
        if self.where_clauses:
            where_clause = ' AND '.join(self.where_clauses)
            query += f" WHERE {where_clause}"
        if hasattr(self, 'group_by_clause'):
            query += f" GROUP BY {self.group_by_clause}"
        return query


'''
    def create_trigger(self, trigger_name: str, trigger_body: str) -> None:
        self.query_executor.create_trigger(trigger_name, trigger_body)
    
    def drop_trigger(self, trigger_name: str) -> None:
        self.query_executor.drop_trigger(trigger_name)

    def create_constraint(self, table_name: str, constraint_name: str, constraint_body: str) -> None:
        self.query_executor.create_constraint(table_name, constraint_name, constraint_body)
    
    def drop_constraint(self, table_name: str, constraint_name: str, column_name: str) -> None:
        self.query_executor.drop_constraint(table_name, constraint_name, column_name)

    def create_transaction(self, transaction_queries: list[str]) -> None:
        self.query_executor.create_transaction(transaction_queries)
    
    def create_stored_procedure(self, procedure_name: str, procedure_body: str) -> None:
        self.query_executor.create_stored_procedure(procedure_name, procedure_body)
    
    def call_stored_procedure(self, procedure_name: str, procedure_params: tuple) -> None:
        self.query_executor.call_stored_procedure(procedure_name, procedure_params)

    def drop_stored_procedure(self, procedure_name: str) -> None:
        self.query_executor.drop_stored_procedure(procedure_name)

    def create_function(self, function_name: str, function_body: str) -> None:
        self.query_executor.create_function(function_name, function_body)
    
    def drop_function(self, function_name: str) -> None:
        self.query_executor.drop_function(function_name)

    def execute_query_by_title(self, query_title: str, *args: str) -> None:
        self.query_executor.execute_query_by_title(query_title, *args)
'''

if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
