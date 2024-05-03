# Purpose: TXT File Manager module for handling TXT file operations.

# Standard Libraries
import io
import os

# Third-party Libraries
import pandas as pd

# Local Modules
from import_modules.web_scraper import WebScraper

# Configure logging
import logging


# TXTFileManager class for handling TXT file operations
class TXTFileManager:
    def __init__(self):
        self.__header: list[str] = []
        self.__data: list[list[str]] = []
        self.__first_column_in_header: str | None = None
        self.__delimiter: str | None = None
        self.__web_scraper = WebScraper(user_agent=True)
    
    def get_header(self) -> list[str]:
        return self.__header
    
    def set_header(self, header: list[str]) -> None:
        self.__header = header
    
    def get_data(self) -> list[list[str]]:
        return self.__data
    
    def get_first_column_in_header(self) -> str | None:
        return self.__first_column_in_header

    def set_first_column_in_header(self, first_column_in_header: str) -> None:
        self.__first_column_in_header = first_column_in_header
    
    def set_delimiter(self, delimiter: str) -> None:
        self.__delimiter = delimiter
    
    def set_data(self, data: list[list[str]]) -> None:
        self.__data = data

    def __find_header_row(self, txt_content: list[list[str]]) -> int | None:
        for i, row in enumerate(txt_content):
            if row and row[0] == self.__first_column_in_header:
                return i
        return None

    def read_txt_file(self, file_path: str) -> list:
        data = []
        with open(file_path, mode="r") as txt_file:
            for row in txt_file:
                row_data = row.split(self.__delimiter)
                data.append(row_data)
        
        # Find the header row
        header_index = self.__find_header_row(data)

        # Check if the header row was found
        if header_index is None:
            raise ValueError(f"Header row with first column '{self.__first_column_in_header}' not found.")

        self.__header = data.pop(header_index)
        self.__data = data
        return data

    def write_txt_file(self, file_path: str, mode: str="append_unique") -> None:
        file_exists = os.path.exists(file_path)
        if file_exists and mode == "append_unique":
            existing_data = self.read_txt_file(file_path)
            new_data = [row for row in self.__data if row not in existing_data]
        else:
            new_data = self.__data

        with open(file_path, mode="w" if mode == "overwrite" else "a") as txt_file:
            if not file_exists or mode == "overwrite":
                if self.__delimiter is None:
                    self.__delimiter = "\t" if "\t" in self.__header else ","
                txt_file.write(self.__delimiter.join(self.__header) + "\n")
            for row in new_data:
                if self.__delimiter is None:
                    self.__delimiter = "\t" if "\t" in row else ","
                txt_file.write(self.__delimiter.join(row) + "\n")
    
    def append_unique_entry_to_txt_file(self, file_path: str, entry: list) -> None:
        file_exists = os.path.exists(file_path)
        if file_exists:
            existing_data = self.read_txt_file(file_path)
            if entry not in existing_data:
                with open(file_path, mode="a") as txt_file:
                    if self.__delimiter is None:
                        self.__delimiter = "\t" if "\t" in entry else ","
                    txt_file.write(self.__delimiter.join(entry) + "\n")
        else:
            with open(file_path, mode="w") as txt_file:
                if self.__delimiter is None:
                    self.__delimiter = "\t" if "\t" in entry else ","
                txt_file.write(self.__delimiter.join(entry) + "\n")
    
    def read_txt_from_url(self, url: str) -> None:
        # Read the TXT file from the URL
        content = self.__web_scraper.get_html_content_as_text(url)
        # logging.debug(f"Content: {content}")
        # Convert the TXT file to a list of lists
        txt_file = io.StringIO(content)
        # Read the TXT file into a list of lists
        data = []
        # logging.debug(f"Delimiter: {self.__delimiter}")
        for row in txt_file:
            # logging.debug(f"Row: {row}")
            row_data = row.strip().split(self.__delimiter)
            data.append(row_data)

        # Find the header row
        # logging.debug(f"First row in data: {data[0]}")
        header_index = self.__find_header_row(data)

        # Check if the header row was found
        if header_index is None:
            raise ValueError(f"Header row with first column '{self.__first_column_in_header}' not found.")
        
        # Remove all rows before the header row
        if header_index > 0:
            # logging.debug(f"Removing {header_index} rows before the header row.")
            # logging.debug(f"Data: {data[:header_index]}")
            data = data[header_index:]
        self.__header = data.pop(0)
        self.__data = data
        # logging.debug(f"Header: {self.__header}")
        # logging.debug(f"Data: {data}")

    # def sort_data_by_column(self, column_name: str) -> None:
    #     column_index = self.__header.index(column_name)
    #     try:
    #         self.__data.sort(key=lambda row: row[column_index])
    #     except IndexError as e:
    #         print(f"Error: {e}")
    #         print("The row causing the error:")
    #         for row in self.__data:
    #             try:
    #                 value = row[column_index]
    #             except IndexError:
    #                 print(row)
    #                 break

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.__data, columns=self.__header)
        return df


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
