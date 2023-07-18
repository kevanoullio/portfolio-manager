# Purpose: ImportEmailAccount class for data retrieval from email account.

# Standard Libraries
import csv
import email
import imaplib
import os

# Third-party Libraries
from html.parser import HTMLParser

# Local Modules
from account_management.email_account import EmailAccount
from account_management.user_account import UserAccount
from import_modules.csv_file_handler import CSVFileHandler
from import_modules.uid_handler import UIDHandler
from session.session_manager import SessionManager

# Configure logging
import logging


# Global variables
last_uid_cache = None

    
# Class to handle IMAP connection and login
class IMAPClient:
    def __init__(self, email_account: EmailAccount | None) -> None:
        self.email_account = email_account
        self.mail = None
        self.servers = {
            "outlook": "outlook.office365.com",
            "gmail": "imap.gmail.com",
            "yahoo": "imap.mail.yahoo.com",
            "aol": "imap.aol.com",
            "icloud": "imap.mail.me.com"
        }


    def login(self):
        if self.email_account is None:
            print("Please set email account first.")
            return None
        
        # Store email address and password into more concise variables
        email_address = self.email_account.address
        password_hash = self.email_account.password_hash

        # Need to check if email address and password are None for decode() to work
        if email_address is None or password_hash is None:
            print("Please set email account first.")
            return None

        # Get the email type from the email address
        email_service = email_address.split("@")[-1].split(".")[0]
        if email_service not in self.servers:
            print("Email service provider not supported for import.")
            return None
        else:
            try:
                self.mail = imaplib.IMAP4_SSL(email_service)
                self.mail.login(email_address, password_hash.decode())
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
                self.mail = self.login()
                if self.mail is None:
                    return []
                return self.list_folders()
        else:
            print("Please login first.")
            return []


    # Method to select a folder and check for new emails
    def select_folder(self, folder_name):
        if self.mail is not None:
            try:
                typ, data = self.mail.select(folder_name)
                return data[0]
            except imaplib.IMAP4.abort:
                print("Failed to select folder. Attempting re-login...")
                self.mail.logout()
                self.mail = self.login()
                if self.mail is None:
                    return None
                return self.select_folder(folder_name)
        else:
            print("Please login first.")
            return None


    # Method to search for emails in a folder
    def search_emails(self, search_query) -> list:
        if self.mail is not None:
            try:
                typ, search_data = self.mail.uid("search", search_query)
                return search_data[0].split()
            except imaplib.IMAP4.abort:
                print("Failed to search for emails. Attempting re-login...")
                self.mail.logout()
                self.mail = self.login()
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








# TODO - make this function a class object?
def import_from_email_account(session_manager: SessionManager) -> int:
    if session_manager.current_user is None or session_manager.current_user.user_id is None:
        return 1
    
    # Fetch all email addresses of usage "import" from the user
    user_email_accounts = session_manager.database.query_executor.get_all_user_email_accounts(session_manager.current_user.user_id)
    import_email_accounts = []

    # Check if any email addresses are found
    if user_email_accounts is None or len(user_email_accounts) == 0:
        print("No email accounts found.")
        return 2
    
    # Filter the email addresses by usage "import"
    for email_account in user_email_accounts:
        if email_account.usage == "import":
            import_email_accounts.append(email_account)
    
    # Check if any import email addresses are found
    if import_email_accounts is None or len(import_email_accounts) == 0:
        print("No email accounts found.")
        return 2



    # TODO - Use AvailableEmailAccount class instead
    # Print the email addresses found
    print("\nAVAILABLE EMAIL ACCOUNTS:")
    print("-------------------------")
    available_email_addresses: list[str] = []
    for available_email_account in import_email_accounts:
        print(available_email_account.address)
        available_email_addresses.append(available_email_account.address)

    # Ask the user to select an email address
    selected_email_address = input("\nEnter the email address to import from: ")
    while selected_email_address not in available_email_addresses:
        selected_email_address = input("Invalid email address. Please try again: ")




    # Get the selected email account
    selected_email_account = None
    for email_account in import_email_accounts:
        if email_account.address == selected_email_account:
            selected_email_account = email_account
            break

    # Login to the IMAP server using the selected email account
    imap_client = IMAPClient(selected_email_account)
    mail = imap_client.login()
    if mail is None:
        return 3




    # TODO - replace with AvailableFolder class
    # List available folders
    folder_list = imap_client.list_folders()
    print("------------------")
    print("Available folders:")
    for folder in folder_list:
        print(folder)
    print("------------------")




    # TODO - Replace with UserInput class
    folder_name = input("Enter the folder name: ")

    # Select the specified folder
    select_result = imap_client.select_folder(folder_name)
    if not select_result:
        print(f"Failed to select folder: {folder_name}")
        return 1
    


    # TODO - change from .csv to directly into the database
    # Set the names of the CSV files to save the data to
    csv_file_sec = "./data/ws-securities.csv"
    csv_file_divs = "./data/ws-divs.csv"
    csv_file_crypto = "./data/ws-crypto.csv"




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
            mail = imap_client.login()
            if mail is None:
                return 1
            typ, data = mail.uid("FETCH", num, "(RFC822)")

        # If the type of the response is not OK, skip the email
        if typ != "OK":
            # The return value of the mail.uid function is a tuple containing two elements.
            # The first element is a string that indicates the status of the command execution
            # ('OK' if the command was successful, or 'NO' or 'BAD' if there was an error). The
            # 2nd element is a list of data returned by the server in response to the command.
            print(f"Error fetching email, typ: {typ}")
            continue

        # If the data is None, skip the email
        if data is None:
            print(f"Error fetching email, data is None")
            continue
        # If the data[0] is None, skip the email
        if data[0] is None:
            print(f"Error fetching email, data[0] is None")
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
            print(f"Email subject did not match any of the expected subjects: {subject}")
        else:
            # Write to csv
            print(data)
            CSVFileHandler.write_to_csv(data, csv_file)

        # Save the UID of the last processed email to a file
        last_uid = num.decode("utf-8")
        UIDHandler.save_last_uid(last_uid)

    print("No new emails to process")

    # Close the connection to the Outlook IMAP server
    mail.close()
    mail.logout()

    return 0


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
