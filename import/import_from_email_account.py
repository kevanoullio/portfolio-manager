# # Purpose: ImportEmailAccount class for data retrieval from email account.

# # Standard Libraries

# # Third-party Libraries

# # Local Modules
# from database.database import Database

# # Class Definitions
# class ImportEmailAccount:
#     def __init__(self, database: Database):
#         self.database = database
#         self.__email = None
#         self.__email_password = None

    
#     def import_email_account(self) -> int:
#         print("Importing an email account...")
        
#         email = input("Enter your email: ")
#         # Check if the email already exists
#         if self.database.email_exists(email):
#             print("Email already exists. Email account import failed.")
#             return 1
        
#         email_password = getpass("Enter your email password: ")
#         confirm_email_password = getpass("Confirm your email password: ")
#         # Check if the email password and confirm_email_password match
#         if email_password != confirm_email_password:
#             print("Email passwords do not match. Email account import failed.")
#             return 2

#         # Import the email account
#         self.__email = email
#         self.__email_password = email_password
#         self.database.store_email_and_password(self.__email, self.__email_password)
#         print("Email account import successful.")
#         return 0