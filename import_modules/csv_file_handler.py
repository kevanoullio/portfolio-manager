# Purpose: CSV File Handler module for handling CSV file operations.

# Standard Libraries
import csv
import os

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# CSVFileHandler class for handling CSV file operations.
class CSVFileHandler:
    @staticmethod
    def open_csv_file(csv_file, mode, fieldnames=None):
        if not os.path.exists(csv_file):
            with open(csv_file, "w") as f:
                if fieldnames:
                    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
                    writer.writeheader()
        return open(csv_file, mode)


    @staticmethod
    def write_to_csv(data: dict, csv_file) -> None:
        with CSVFileHandler.open_csv_file(csv_file, "a", fieldnames=data.keys()) as f:
            writer = csv.DictWriter(f, fieldnames=data.keys(), lineterminator="\n")
            writer.writerow(data)



def find_header_position(csv_data: str, header_first_column: str) -> int:
    # Convert the CSV data to a list of lines
    lines = csv_data[:1000].strip().split("\n")
    
    # Iterate through the lines to find the header
    for i, line in enumerate(lines[:10]):
        if header_first_column in line:
            return i
    
    # If the header is not found, return -1
    return -1

def parse_csv(csv_data: str, header_first_column: str) -> list[dict]:
    header_position = find_header_position(csv_data, header_first_column)
    if header_position == -1:
        raise ValueError("Header not found in CSV data.")
    
    # Split the CSV data into lines and remove empty lines
    lines = csv_data.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    
    # Extract the header and data based on the header position
    header = lines[header_position]
    data = lines[header_position + 1:]

    # Parse the CSV data using csv.DictReader and specify the fieldnames (header)
    reader = csv.DictReader(data, delimiter=",", fieldnames=header.split(","))
    next(reader)  # Skip the header row
    result = [row for row in reader]
    
    return result


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
