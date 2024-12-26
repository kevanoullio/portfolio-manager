# Purpose: Accounts module for defining various account data types.

# Standard Libraries
from dataclasses import dataclass

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# UserAccount class for defining user account data type
@dataclass
class UserAccount:
    user_id: int # TODO - store user_role?
    username: str
    password_hash: bytes | None = None

    def __post_init__(self) -> None:
        logging.info(f"User initialized successfully. Username: {self.username}, User ID: {self.user_id}")

    def __str__(self) -> str:
        return f"User ID: {self.user_id}, Username: {self.username}"


# EmailAccount class for defining email account data type
@dataclass
class EmailAccount:
    usage: str
    address: str
    password_hash: bytes | None = None

    def __post_init__(self) -> None:
        logging.info(f"Email account initialized successfully. Address: {self.address}, Usage: {self.usage}")

    def __str__(self) -> str:
        return f"Email Address: {self.address}, Usage: {self.usage}"


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
