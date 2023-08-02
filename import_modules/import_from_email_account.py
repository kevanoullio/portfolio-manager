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
from html.parser import HTMLParser

# Local Modules
from database_management.database import Database
from import_modules.csv_file_manager import CSVFileManager
from import_modules.uid_handler import UIDHandler

# Local modules imported for Type Checking purposes only
if TYPE_CHECKING:
    from account_management.accounts import UserAccount, EmailAccount

# Configure logging
import logging


# Global variables
last_uid_cache = None

    
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


# TODO - make this function a class object???
def import_from_email_account(database: Database) -> int:
    from user_interface.user_input import UserInput
    user_input = UserInput()
    # Fetch all email addresses of usage "import" from the user
    import_email_accounts = database._query_executor.get_user_email_accounts_by_usage("import")
    
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
    selected_import_email_account_password_hash = database._query_executor.get_email_account_password_hash_by_email_address(selected_import_email_account.address)

    # Check if the selected email account's password hash is found
    if selected_import_email_account_password_hash is None:
        print("Error: Email account password not found in the database. Please ensure you've properly added an email account for importing porfolios.")
        return 2

    # Validate the user's email credentials
    from account_management.account_operations import UserAccountOperation, EmailAccountOperation
    from access_management.account_authenticator import AccountAuthenticator
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

    # TODO - replace with AvailableFolder menu class???
    # List available folders
    folder_list = imap_client.list_folders()
    title = "Available folders:"
    print(f"\n{title}")
    print("-" * len(title))
    for folder in folder_list:
        print(folder)
    print("\n")

    # TODO - Replace with UserInput class???
    folder_name = input("Enter the folder name (copy/paste from above): ")

    # Select the specified folder
    select_result = imap_client.select_folder(folder_name)
    if not select_result:
        print(f"Failed to select folder: {folder_name}")
        return 1
    
    print(f"Scanning emails from '{selected_import_email_account.address}' in the '{folder_name}' folder...")
    


    # TODO - change from .csv to directly into the database
    # Set the names of the CSV files to save the data to
    csv_file_sec = "./old_data/ws-securities.csv"
    csv_file_divs = "./old_data/ws-divs.csv"
    csv_file_crypto = "./old_data/ws-crypto.csv"




    # Read the UID of the last processed email from the file
    last_uid = UIDHandler.read_last_uid()

    # Search for emails with a UID greater than the last processed email in the selected folder
    if last_uid is not None:
        search_query = f"UID {int(last_uid) + 1}:*"
    else:
        search_query = "ALL"

    search_data = imap_client.search_emails(search_query)
    if not search_data:
        print("No emails found.")
        return 1

    for num in search_data:
        if num.decode("utf-8") == last_uid:
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
        csv_file = ""

        # Check if the email is a crypto or security email
        if ("order" and "filled") in subject.lower():
            # Specify the desired order of the keys and initialize their values
            data = {"Date (UTC)" : date, "Account" : "", "Type" : "", "Symbol" : "", "Shares" : "", "Average price" : "", "Total" : ""}
            # Extract the data from the email body
            data = extract_from_email(data, body)
            # Check if the email is a crypto email
            if "Cryptocurrency" in body:
                csv_file = csv_file_crypto
            # Otherwise, it is a security email
            else:
                csv_file = csv_file_sec
        # Check if the email is a dividend email
        elif ("You" and "a dividend") in subject.lower():
            csv_file = csv_file_divs
            # Specify the desired order of the keys and initialize their values
            data = {"Date (UTC)" : date, "Account" : "", "Type" : "Dividend", "Symbol" : "", "Amount" : ""}
            # Extract the data from the email body
            data = extract_from_email(data, body)
        
        if not csv_file:
            logging.info(f"Email subject did not match any of the expected subjects: {subject}")
        else:
            # Write to csv
            logging.debug(data)
            csv_file_manager = CSVFileManager()
            csv_file_manager.set_header(list(data.keys()))
            csv_file_manager.set_first_column_in_header(list(data.keys())[0])
            csv_file_manager.append_unique_entry_to_csv_file(csv_file, list(data.values()))

        # Save the UID of the last processed email to a file
        last_uid = num.decode("utf-8")
        UIDHandler.save_last_uid(last_uid)

    print("No new emails to process.")
    print("Import complete!")

    # Close the connection to the Outlook IMAP server
    mail.close()
    mail.logout()

    return 0


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
