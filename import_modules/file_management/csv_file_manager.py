# Purpose: CSV File Manager module for handling CSV file operations.

# Standard Libraries
import csv
import io
import os

# Third-party Libraries
import pandas as pd

# Local Modules
from import_modules.web_scraper import WebScraper

# Configure logging
import logging


# CSVFileManager class for handling CSV file operations
class CSVFileManager:
    def __init__(self):
        self._header: list[str] = []
        self._data: list[list[str]] = []
        self._first_column_in_header: str | None = None
        self._web_scraper = WebScraper(user_agent=True)
    
    def get_header(self) -> list[str]:
        return self._header
    
    def set_header(self, header: list[str]) -> None:
        self._header = header
    
    def get_data(self) -> list[list[str]]:
        return self._data
    
    def get_first_column_in_header(self) -> str | None:
        return self._first_column_in_header

    def set_first_column_in_header(self, first_column_in_header: str) -> None:
        self._first_column_in_header = first_column_in_header
    
    def set_data(self, data: list[list[str]]) -> None:
        self._data = data

    def _find_header_row(self, csv_content: list[list[str]]) -> int | None:
        for i, row in enumerate(csv_content):
            if row and row[0] == self._first_column_in_header:
                return i
        return None

    def read_csv_file(self, file_path: str) -> list:
        with open(file_path, mode="r") as csv_file:
            reader = csv.reader(csv_file)
            data = [row for row in reader]
        
        # Find the header row
        header_index = self._find_header_row(data)

        # Check if the header row was found
        if header_index is None:
            raise ValueError(f"Header row with first column '{self._first_column_in_header}' not found.")

        self._header = data.pop(header_index)
        self._data = data
        return data

    def write_csv_file(self, file_path: str, mode: str="append_unique") -> None:
        file_exists = os.path.exists(file_path)
        if file_exists and mode == "append_unique":
            existing_data = self.read_csv_file(file_path)
            new_data = [row for row in self._data if row not in existing_data]
        else:
            new_data = self._data

        with open(file_path, mode="w" if mode == "overwrite" else "a") as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists or mode == "overwrite":
                writer.writerow(self._header)
            for row in new_data:
                writer.writerow(row)
    
    def append_unique_entry_to_csv_file(self, file_path: str, entry: list) -> None:
        file_exists = os.path.exists(file_path)
        if file_exists:
            existing_data = self.read_csv_file(file_path)
            if entry not in existing_data:
                with open(file_path, mode="a") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(entry)
        else:
            with open(file_path, mode="w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(self._header)
                writer.writerow(entry)
    
    def read_csv_from_url(self, url: str) -> None:
        # Read the CSV file from the URL
        content = self._web_scraper.get_html_content_as_text(url)
        # Convert the CSV file to a list of lists
        csv_file = io.StringIO(content)
        # Read the CSV file into a list of lists
        reader = csv.reader(csv_file)
        data = [row for row in reader]

        # Find the header row
        header_index = self._find_header_row(data)

        # Check if the header row was found
        if header_index is None:
            raise ValueError(f"Header row with first column '{self._first_column_in_header}' not found.")
        
        # Remove all rows before the header row
        if header_index > 0:
            logging.debug(f"Removing {header_index} rows before the header row.")
            logging.debug(f"Data: {data[:header_index]}")
            data = data[header_index:]
        self._header = data.pop(0)
        self._data = data
        logging.debug(f"Header: {self._header}")
        logging.debug(f"Data: {data}")

    def sort_data_by_column(self, column_name: str) -> None:
        column_index = self._header.index(column_name)
        self._data.sort(key=lambda row: row[column_index])

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self._data, columns=self._header)
        return df


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
