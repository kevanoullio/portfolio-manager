# Purpose: UID Handler module for handling Unique Identifier (UID) operations.

# Standard Libraries
import os

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# UIDHandler class for handling Unique Identifier (UID) operations.
class UIDHandler:
    @staticmethod
    # Function for saving the UID of the last processed email to a file
    def save_last_uid(uid):
        try:
            with open("./data/last_uid.txt", "w") as f:
                f.write(str(uid))
        except Exception as e:
            print(f"Error saving last UID: {e}")

    
    @staticmethod
    # Define a function to read the UID of the last processed email from a file
    def read_last_uid(last_uid_cache: str | None = None):
        global last_uid_cache
        if last_uid_cache is not None:
            return last_uid_cache
        if os.path.isfile("./data/last_uid.txt") and os.path.getsize("./data/last_uid.txt") > 0:
            try:
                with open("./data/last_uid.txt", "r") as f:
                    last_uid = f.read()
                    last_uid_cache = last_uid
                    return last_uid
            except Exception as e:
                print(f"Error reading last UID: {e}")
        return None


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
