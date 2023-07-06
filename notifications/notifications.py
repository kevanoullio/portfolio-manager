# Purpose: Notification class for managing notifications.

# Standard Libraries

# Third-party Libraries

# Local Modules
from database.database import Database

# Notifications class
class Notifications:
    def __init__(self, database: Database):
        self.database = database

    def add_email_column(self):
        self.database.add_email_column()