# Purpose: Notification class for managing notifications.

# Standard Libraries

# Third-party Libraries

# Local Modules
from data_management.database import Database

# Notifications class
class Notifications:
    def __init__(self, database: Database):
        self.database = database
