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


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
