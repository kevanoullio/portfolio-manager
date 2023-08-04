# Purpose: ImportEmailAccount class for data retrieval from email account.

# Type Checking
from __future__ import annotations
from typing import TYPE_CHECKING

# Standard Libraries
import csv
import email
import imaplib
import os

# Third-party Libraries
import pandas as pd
from html.parser import HTMLParser
import yfinance as yf

# Local Modules
from database_management.database import Database
from import_modules.csv_file_manager import CSVFileManager
from import_modules.uid_handler import UIDHandler
from database_management.schema.schema import AssetInfo, AssetTransaction
from account_management.account_operations import UserAccountOperation, EmailAccountOperation
from access_management.account_authenticator import AccountAuthenticator

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# Global variables
last_uid_cache: int | None = None

    
# Class to handle IMAP connection and login
class IMAPClient:
    def __init__(self, email_address: str, email_account_password_hash: bytes) -> None:
        self.email_address = email_address
        self.email_account_password_hash = email_account_password_hash
        self.mail = None
        self.server_hosts = {
            "outlook": "outlook.office365.com",
            "gmail": "imap.gmail.com",
            "yahoo": "imap.mail.yahoo.com",
            "aol": "imap.aol.com",
            "icloud": "imap.mail.me.com"
        }

    def email_login(self) -> imaplib.IMAP4_SSL | None:
        # Need to check if email address and password are None for decode() to work
        if self.email_address is None or self.email_account_password_hash is None:
            print("Please set email account first.")
            return None

        # Get the email type from the email address
        email_service_host = self.email_address.split("@")[-1].split(".")[0]
        if email_service_host not in self.server_hosts:
            print("Email service provider not supported for import.")
            return None
        else:
            try:
                self.mail = imaplib.IMAP4_SSL(self.server_hosts[email_service_host])
                self.mail.login(self.email_address, self.email_account_password_hash.decode())
                return self.mail
            except imaplib.IMAP4.error:
                print("Failed to login. Please check your credentials.")
                self.mail = None  # Reset the mail object to None upon login failure
                return None
    
    # Method to list all folders in the mailbox
    def list_folders(self) -> list:
        if self.mail is not None:
            try:
                typ, folder_list = self.mail.list()
                folders = []
                for folder_data in folder_list:
                    if folder_data is not None:
                        if isinstance(folder_data, bytes):
                            decoded_folder = folder_data.decode()
                        else:
                            decoded_folder = folder_data[1].decode()
                        folder_name = decoded_folder.split(' "/" ')[-1]
                        folders.append(folder_name)
                return folders
            except (imaplib.IMAP4.abort, AttributeError):
                print("Failed to retrieve folder list. Attempting re-login...")
                self.mail.logout()
                self.mail = self.email_login()
                if self.mail is None:
                    return []
                return self.list_folders()
        else:
            print("Please login first.")
            return []

    # Method to select a folder and check for new emails
    def select_folder(self, folder_name: str):
        if self.mail is not None:
            try:
                typ, data = self.mail.select(folder_name)
                return data[0]
            except imaplib.IMAP4.abort:
                print("Failed to select folder. Attempting re-login...")
                self.mail.logout()
                self.mail = self.email_login()
                if self.mail is None:
                    return None
                return self.select_folder(folder_name)
        else:
            print("Please login first.")
            return None

    # Method to search for emails in a folder
    def search_emails(self, search_query: str) -> list:
        if self.mail is not None:
            try:
                typ, search_data = self.mail.uid("search", search_query)
                return search_data[0].split()
            except imaplib.IMAP4.abort:
                print("Failed to search for emails. Attempting re-login...")
                self.mail.logout()
                self.mail = self.email_login()
                if self.mail is None:
                    return []
                return self.search_emails(search_query)
        else:
            print("Please login first.")
            return []


# Function to extract the data from the email body
def extract_from_email(data: dict, email_body) -> dict:
    email_body_split = email_body.splitlines()
    total_found = False  # Flag to track if "Total cost" or "Total value" is found

    for line in email_body_split:
        if ":" in line and "https" not in line and "mailto" not in line:
            key, value = line.split(":", 1)
            key = key.strip().replace("*", "")
            value = value.strip().replace("*", "")

            if "Account" in key and len(key) > 7:
                key = "Account"

            transformations = {
                "Cryptocurrency": "Symbol",
                "Total cost": "Total",
                "Total value": "Total"
            }

            if key in data:
                data[key] = value
            elif key in transformations:
                data[transformations[key]] = value

            # Check if "Total cost" or "Total value" is found
            if key == "Total cost" or key == "Total value":
                total_found = True

    if not total_found and data.get("Quantity") and data.get("Average price"):
        split_value = data["Average price"].split("$")
        formatted_total = "{:.2f}".format(float(data["Quantity"]) * float(split_value[1]))
        data["Total"] = split_value[0] + "$" + formatted_total

        split_value = data["Average price"].split("$")
        quantity = float(data["Quantity"].replace(",", ""))
        price = float(split_value[1].replace(",", ""))
        total = quantity * price
        formatted_total = "${:,.2f}".format(total)
        data["Total"] = split_value[0] + formatted_total

    return data


# Class definition for parsing HTML
class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""

    def feed(self, data):
        self.text = ""
        super().feed(data)

    def handle_data(self, data):
        self.text += data


# AssetInfoExtractor class for extracting asset information from yahoo finance
class AssetInfoExtractor:
    def __init__(self, database: Database) -> None:
        self._database = database
        self._asset_info: AssetInfo | None = None

    def get_asset_class_id(self, asset_class: str) -> int | None:
        return self._database.query_executor.get_asset_class_id_by_asset_class_name(asset_class)
    
    def get_sector_id_or_insert(self, sector: str) -> int | None:
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector)
        if sector_id is None:
            self._database.query_executor.insert_sector(sector)
        sector_id = self._database.query_executor.get_sector_id_by_sector_name(sector)
        return sector_id
    
    def get_industry_id_or_insert(self, industry: str) -> int | None:
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry)
        if industry_id is None:
            self._database.query_executor.insert_industry(industry)
        industry_id = self._database.query_executor.get_industry_id_by_industry_name(industry)
        return industry_id
    
    def get_country_id_by_country_name(self, country: str) -> int | None:
        return self._database.query_executor.get_country_id_by_country_name(country)
    
    def get_currency_id_by_currency_iso_code(self, currency_iso_code: str) -> int | None:
        return self._database.query_executor.get_currency_id_by_currency_iso_code(currency_iso_code)
    
    def get_exchange_id_by_exchange_acronym(self, exchange_acronym: str) -> int | None:
        return self._database.query_executor.get_exchange_id_by_exchange_acronym(exchange_acronym)
    
    def get_asset_info_from_yf(self, asset_symbol: str) -> dict[str, str | int] | None:
        df_asset_info = yf.Ticker(asset_symbol).info
        if df_asset_info:
            asset_info_dict = {
                "asset_class": df_asset_info.get("quoteType"),
                "sector": df_asset_info.get("sector"),
                "industry": df_asset_info.get("industry"),
                "country": df_asset_info.get("country"),
                "city": df_asset_info.get("city"),
                "currency": df_asset_info.get("currency"),
                "exchange": df_asset_info.get("exchange"),
                "symbol": asset_symbol,
                "company_name": df_asset_info.get("shortName")
            }
            for item in asset_info_dict:
                if asset_info_dict[item] is None:
                    asset_info_dict[item] = ""
            return asset_info_dict
        else:
            return None


# AssetTransactionManager class for managing asset transactions
class AssetTransactionManager:
    def __init__(self, database: Database):
        self._database = database
        self._asset_transactions: list[AssetTransaction] = []  # Initialize as an empty list

    def get_asset_id(self, asset_symbol: str) -> int | None:
        return self._database.query_executor.get_asset_id_by_asset_symbol(asset_symbol)

    def get_transaction_type_id(self, transaction_type: str) -> int | None:
        return self._database.query_executor.get_transaction_type_id_by_transaction_type_name(transaction_type)

    def get_brokerage_id_or_insert(self, brokerage_name: str) -> int | None:
        brokerage_id = self._database.query_executor.get_brokerage_id_by_brokerage_name(brokerage_name)
        if brokerage_id is None:
            self._database.query_executor.insert_brokerage(brokerage_name)
        brokerage_id = self._database.query_executor.get_brokerage_id_by_brokerage_name(brokerage_name)
        return brokerage_id

    def get_asset_account_id(self, asset_account_name: str) -> int | None:
        return self._database.query_executor.get_asset_account_id_by_asset_account_name(asset_account_name)

    def append_asset_transaction(self, asset_transaction: AssetTransaction) -> None:
        # Append the new transaction to the list of asset transactions
        self._asset_transactions.append(asset_transaction)

    def convert_asset_transactions_to_dataframe(self) -> pd.DataFrame:
        # Convert the list of objects to a list of dictionaries
        transactions_dict = [t.to_dict() for t in self._asset_transactions]
        # Convert the list of dictionaries to a dataframe
        return pd.DataFrame(transactions_dict)


# TODO - make this function a class object???
def import_from_email_account(database: Database) -> int:
    from user_interface.user_input import UserInput
    user_input = UserInput()
    # Fetch all email addresses of usage "import" from the user
    import_email_accounts = database.query_executor.get_user_email_accounts_by_usage("import")
    
    # Check if any import email addresses are found
    if import_email_accounts is None or len(import_email_accounts) <= 0:
        print("No email accounts for importing portfolios found.")
        print("Please add an email account in the account settings.")
        return 1

    # TODO - Replace with AvailableEmailAccount class???
    # Print the available email accounts
    title = "AVAILABLE EMAIL ACCOUNTS:"
    print(f"\n{title}")
    print("-" * len(title))
    for i, email_account in enumerate(import_email_accounts, start=1):
        print(f"{i}: {email_account.address}")

    # Get the user's choice
    choice = user_input.get_valid_menu_choice(len(import_email_accounts), "Choose the email account you would like to import from: ")
    # Get the email account based on the user's choice
    selected_import_email_account = import_email_accounts[choice - 1]

    # Prompt the user for the email account password
    provided_password_hash = user_input.password_prompt(prompt="Verify your email credentials by entering your email password: ", confirm=False)
    # Get the selected email account's password hash
    selected_import_email_account_password_hash = database.query_executor.get_email_account_password_hash_by_email_address(selected_import_email_account.address)

    # Check if the selected email account's password hash is found
    if selected_import_email_account_password_hash is None:
        print("Error: Email account password not found in the database. Please ensure you've properly added an email account for importing porfolios.")
        return 2

    # Validate the user's email credentials
    user_account_operation = UserAccountOperation(database)
    email_account_operation = EmailAccountOperation(database)
    email_authenticated = AccountAuthenticator(user_account_operation, email_account_operation)
    email_authenticated.validate_email_credentials(selected_import_email_account.address, provided_password_hash)

    if not email_authenticated:
        print("Invalid email credentials.")
        return 3
    # Login to the IMAP server using the selected email account
    imap_client = IMAPClient(selected_import_email_account.address, provided_password_hash)
    mail = imap_client.email_login()
    if mail is None:
        return 3

    # List available folders
    folder_list = imap_client.list_folders()
    title = "Available folders:"
    print(f"\n{title}")
    print("-" * len(title))
    for folder in folder_list:
        print(folder)
    print("\n")

    folder_name = input("Enter the folder name (copy/paste from above): ")

    # Select the specified folder
    select_result = imap_client.select_folder(folder_name)
    if not select_result:
        print(f"Failed to select folder: {folder_name}")
        return 1

    # Create a new AssetTransactionManager object
    asset_transaction_manager = AssetTransactionManager(database)

    # Prompt the user for the brokerage
    brokerage_name = input("Enter the brokerage name: ")
    brokerage_id = asset_transaction_manager.get_brokerage_id_or_insert(brokerage_name)
    if brokerage_id is None:
        print("Failed to get brokerage ID.")
        return 1

    print(f"Scanning '{brokerage_name}' emails from '{selected_import_email_account.address}' in the '{folder_name}' folder...")



    # # TODO - change from .csv to directly into the database
    # # Set the names of the CSV files to save the data to
    # csv_file_sec = "./old_data/ws-securities.csv"
    # csv_file_divs = "./old_data/ws-divs.csv"
    # csv_file_crypto = "./old_data/ws-crypto.csv"


    # Get the UID of the last email in the selected folder
    last_uid = database.query_executor.get_last_uid_by_email_address_and_folder_name(selected_import_email_account.address, folder_name)

    last_uid_cache = last_uid

    # Search for emails with a UID greater than the last processed email in the selected folder
    if last_uid_cache is not None:
        search_query = f"UID {int(last_uid_cache) + 1}:*"
    else:
        search_query = "ALL"

    search_data = imap_client.search_emails(search_query)
    if not search_data:
        print("No emails found.")
        return 1

    for num in search_data:
        if num.decode("utf-8") == last_uid_cache:
            continue
        # Get the email
        try:
            # RFC822 is a standard format for text messages that are sent using the Internet.
            # It specifies the syntax for text messages, including the format of header fields
            # and the structure of the message body.
            typ, data = mail.uid("FETCH", num, "(RFC822)")
            # The mail.uid function is a method of an IMAP4 object that is used to execute a
            # command on the server using a unique identifier (UID) rather than a message
            # sequence number. "FETCH" is used to fetch data associated with a message
            # on the server. "num" is the UID of the message to be fetched, "(RFC822)" specifies
            # which parts of the message you want to fetch.
        except imaplib.IMAP4.abort:
            mail = imap_client.email_login()
            if mail is None:
                return 1
            typ, data = mail.uid("FETCH", num, "(RFC822)")

        # If the type of the response is not OK, skip the email
        if typ != "OK":
            # The return value of the mail.uid function is a tuple containing two elements.
            # The first element is a string that indicates the status of the command execution
            # ('OK' if the command was successful, or 'NO' or 'BAD' if there was an error). The
            # 2nd element is a list of data returned by the server in response to the command.
            logging.info(f"Error fetching email, typ: {typ}")
            continue

        # If the data is None, skip the email
        if data is None:
            logging.info(f"Error fetching email, data is None")
            continue
        # If the data[0] is None, skip the email
        if data[0] is None:
            logging.info(f"Error fetching email, data[0] is None")
            continue

        # Parse the email
        email_message = email.message_from_bytes(data[0][1]) # type: ignore

        # Get the date
        date = email_message.get("Date")

        # Extract the body of the email based on the content type
        body = ""
        if email_message.get_content_type() == "text/plain":
            # Get the charset of the email
            charset = email_message.get_content_charset()
            # Decode the email body
            body = email_message.get_payload(decode=True).decode(charset)
        elif email_message.get_content_type() == "text/html":
            # Get the charset of the email
            charset = email_message.get_content_charset()
            # Decode the email body
            html = email_message.get_payload(decode=True).decode(charset)
            # Use an HTML parser to extract the text from the HTML content
            parser = MyHTMLParser()
            parser.feed(html)
            body = parser.text
        elif email_message.get_content_type() == "multipart/alternative":
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    # Get the charset of the email
                    charset = part.get_content_charset()
                    # Decode the email body
                    body = part.get_payload(decode=True).decode(charset)
                    break

        # Check if the email subject matches one of the subject titles
        subject = email_message["Subject"]

        # Initialize the data dictionary and csv_file
        data = {}

        # Check if the email is a crypto or security email
        if ("order" and "filled") in subject.lower():
            # Specify the desired order of the keys and initialize their values
            data = {"Date (UTC)" : date, "Account" : "", "Type" : "", "Symbol" : "", "Shares" : "", "Average price" : "", "Total" : ""}
            # Extract the data from the email body
            data = extract_from_email(data, body)

        # Check if the email is a dividend email
        elif ("You" and "a dividend") in subject.lower():
            # Specify the desired order of the keys and initialize their values
            data = {"Date (UTC)" : date, "Account" : "", "Type" : "Dividend", "Symbol" : "", "Amount" : ""}
            # Extract the data from the email body
            data = extract_from_email(data, body)
        
        else:
            logging.info(f"Email subject did not match any of the expected subjects: {subject}")

        logging.debug(data)

        # Save the UID of the last processed email to a file
        last_uid_cache = num.decode("utf-8")

    # Update the last processed email UID in the database
    if last_uid_cache is not None:
        database.query_executor.insert_uid_by_email_address_and_folder_name(selected_import_email_account.address, folder_name, last_uid_cache)

    print("No new emails to process.")
    print("Import complete!")

    # Close the connection to the Outlook IMAP server
    mail.close()
    mail.logout()

    return 0


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
