# Purpose: JSON Preset Manager module for managing all json preset operations.

# Standard Libraries
import json

# Third-party Libraries

# Local Modules

# Configure logging
import logging


# # TODO - don't use email preset, store directly in database
# # ---->>> use json preset for other account settings
# # EmailPresetManager class for managing json presets for email accounts and folders
# class EmailPresetManager:
#     def __init__(self):
#         self.presets_file = "./data/presets.json"
#         self.presets = self.load_presets()

#     def load_presets(self):
#         try:
#             with open(self.presets_file, "r") as file:
#                 presets = json.load(file)
#         except (FileNotFoundError, json.JSONDecodeError):
#             presets = {}

#         return presets

#     def save_presets(self):
#         with open(self.presets_file, "w") as file:
#             json.dump(self.presets, file, indent=4)

#     def add_preset(self, email_account, email_folder, uid, keyword):
#         if email_account not in self.presets:
#             self.presets[email_account] = {}

#         if email_folder not in self.presets[email_account]:
#             self.presets[email_account][email_folder] = []

#         # Check if the uid already exists for the email folder
#         for preset in self.presets[email_account][email_folder]:
#             if preset["uid"] == uid:
#                 print("UID already exists for the given email folder. Preset not added.")
#                 return

#         self.presets[email_account][email_folder].append({"uid": uid, "keyword": keyword})
#         self.save_presets()

#     def get_presets(self):
#         return self.presets

#     def get_next_uid(self, email_account, email_folder):
#         if email_account in self.presets and email_folder in self.presets[email_account]:
#             uid_list = self.presets[email_account][email_folder]
#             if uid_list:
#                 next_uid = max(uid_list, key=lambda x: x["uid"])["uid"] + 1
#             else:
#                 next_uid = 0
#         else:
#             next_uid = 0
#         return next_uid

#     def create_new_email_account(self, email_account, email_folder, uid, keyword):
#         if email_account not in self.presets:
#             self.presets[email_account] = {}
#             self.presets[email_account][email_folder] = [{"uid": uid, "keyword": keyword}]
#             self.save_presets()

#     def create_new_email_folder(self, email_account, email_folder, uid, keyword):
#         if email_account in self.presets and email_folder not in self.presets[email_account]:
#             self.presets[email_account][email_folder] = [{"uid": uid, "keyword": keyword}]
#             self.save_presets()


# # Example usage:

# preset_manager = EmailPresetManager()

# # Prompt the user for email data:
# email_account = input("Enter the email account: ")
# email_folder = input("Enter the email folder: ")
# uid = preset_manager.get_next_uid(email_account, email_folder)
# keyword = input("Enter the keyword used in the emails: ")

# # Add the preset if it doesn't exist
# preset_manager.add_preset(email_account, email_folder, uid, keyword)

# # Get all the presets:
# all_presets = preset_manager.get_presets()
# print(all_presets)

# # Create new email account and folder if they don't exist
# email_account_new = input("Enter the new email account: ")
# email_folder_new = input("Enter the new email folder: ")
# uid_new = preset_manager.get_next_uid(email_account_new, email_folder_new)
# keyword_new = input("Enter the keyword used in the emails for the new account/folder: ")

# preset_manager.create_new_email_account(email_account_new, email_folder_new, uid_new, keyword_new)

# # Get all the presets again after adding new account and folder:
# all_presets = preset_manager.get_presets()
# print(all_presets)


if __name__ == "__main__":
    print("This module is not meant to be executed directly.")
