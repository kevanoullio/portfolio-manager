# Purpose: CSV File Manager module for handling CSV file operations.

# Standard Libraries
import csv
import os

# Third-party Libraries
import pandas as pd

# Local Modules

# Configure logging
import logging


# CSVFileManager class for handling CSV file operations
class CSVFileManager:
    def __init__(self):
        self.header = []
        self.data = []

    def _find_header_row(self, header_first_column: str) -> list | None:
        for row in self.data:
            if row and row[0] == header_first_column:
                return row
        return None

    def read_csv_file(self, file_path: str) -> list:
        with open(file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            data = [row for row in reader]
        self.header = data.pop(0)
        self.data = data
        return data

    def write_csv_file(self, file_path: str, mode: str = 'append_unique') -> None:
        file_exists = os.path.exists(file_path)
        if file_exists and mode == 'append_unique':
            existing_data = self.read_csv_file(file_path)
            new_data = [row for row in self.data if row not in existing_data]
        else:
            new_data = self.data

        with open(file_path, mode='w' if mode == 'overwrite' else 'a') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists or mode == 'overwrite':
                writer.writerow(self.header)
            for row in new_data:
                writer.writerow(row)

    def sort_data_by_column(self, column_name: str) -> None:
        column_index = self.header.index(column_name)
        self.data.sort(key=lambda x: x[column_index])

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.data, columns=self.header)
        return df


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
