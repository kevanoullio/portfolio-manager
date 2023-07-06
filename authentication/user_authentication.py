# Purpose: Account class for user authentication and account management.

# Standard Libraries
from getpass import getpass

# Third-party Libraries
import bcrypt

# Local Modules
from database.database import Database


# UserAuthentication class
class UserAuthentication:
    def __init__(self, database):
        self.database = database
        self.logged_in = False
        self.__username = None
        self.__password = None


    def create_account(self) -> int:
        print("Creating a new account...")
        
        username = input("Enter your username: ")
        # Check if the username already exists
        if self.database.username_exists(username):
            print("Username already exists. Account creation failed.")
            return 1
        
        password = getpass("Enter your password: ")
        confirm_password = getpass("Confirm your password: ")
        # Check if the password and confirm_password match
        if password != confirm_password:
            print("Passwords do not match. Account creation failed.")
            return 2

        # Create the account
        self.__username = username
        self.__password = self.__hash_password(password)
        self.database.store_username_and_password(self.__username, self.__password)
        print("Account creation successful.")

        # Log the user in
        self.logged_in = True
        print("Login successful.")
        return 0


    def login(self) -> int:
        if not self.logged_in:
            print("Logging in...")

            username = input("Enter your username: ")
            # Check if the username exists
            if not self.database.username_exists(username):
                print("Account login failed.")
                return 1
            
            password = getpass("Enter your password: ")
            # Retrieve the hashed password from the database
            stored_password_hash = self.database.get_password_hash(username)

            # Verify the entered password
            if bcrypt.checkpw(password.encode(), stored_password_hash):
                print(f"Logging in as {username}...")
                self.logged_in = True
                print("Login successful.")
                return 0
            else:
                print("Password is incorrect. Account login failed.")
                return 2
        else:
            print("You are already logged in.")
            return 0

    
    def logout(self) -> int:
        if self.logged_in:
            # Log the user out
            print("Logging out...")
            self.logged_in = False
            print("Logout successful.")
            return 0
        else:
            print("You are not logged in.")
            return 1


    def __hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password


    def modify_account(self):
        print("Modifying the account...")
        # Code for modifying the account
        # Example: Use a third-party library or API to modify the account
        print("Account modification successful.")


    def delete_account(self):
        print("Deleting the account...")
        # Code for deleting the account
        # Example: Use a third-party library or API to delete the account
        print("Account deletion successful.")
        self.logged_in = False
    

if __name__ == "__main__":
    database = Database("db_file_test.db")

    user_auth = UserAuthentication(database)

    user_auth.create_account()
    user_auth.login()
    user_auth.modify_account()
    user_auth.delete_account()



# To ensure that only logged-in users can access the stored data and that users can only access their own data, you'll need to implement proper authentication and authorization mechanisms in your application. Here are some steps you can follow:

# 1. User Authentication:
#    - Implement a secure user login system where users can provide their credentials (username and password) to authenticate themselves.
#    - Hash and store the passwords securely in the database, as we discussed earlier.
#    - When a user attempts to log in, verify their credentials against the stored hashed password.
#    - Maintain a session or token-based authentication mechanism to keep track of authenticated users.

# 2. User Authorization:
#    - Assign appropriate roles or permissions to each user, such as admin, regular user, etc.
#    - Associate the authenticated user with their respective role or permissions in the system.
#    - Implement authorization checks at various levels, such as for accessing specific functionalities or viewing specific data.

# 3. Data Access Control:
#    - Ensure that each piece of stored data is associated with the corresponding user who owns it.
#    - When storing data in the database, include a reference to the user who owns that data.
#    - Implement appropriate queries and filters to retrieve and display only the data that belongs to the currently authenticated user.
#    - Enforce these data access controls at the application level, ensuring that users can only view and modify their own data.

# 4. Secure Application Design:
#    - Implement secure coding practices to protect against common vulnerabilities like SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF).
#    - Use parameterized queries or ORM (Object-Relational Mapping) frameworks to prevent SQL injection attacks.
#    - Sanitize and validate user input to prevent malicious code execution.
#    - Implement secure session management techniques, such as using session tokens, secure cookies, or JWT (JSON Web Tokens).

# By combining these steps, you can create a robust user authentication and data access control system in your application, ensuring that only authenticated users can access their own data while protecting the privacy and security of the users' information.




##########################




# To ensure that only the corresponding user can access their own data, you can include a `user_id` column in your database tables. This `user_id` column will associate each row of data with the respective user. 

# Here are the steps you can follow:

# 1. Modify the table schema: Add a `user_id` column to the tables that store user-specific data. This column will reference the `id` column in the user table as a foreign key.

# 2. During data insertion: When inserting data into these tables, make sure to include the appropriate `user_id` value that corresponds to the logged-in user. This way, each row of data is associated with the specific user who created it.

# 3. Data retrieval: When fetching data from these tables, include a filtering condition in your SQL queries to retrieve only the rows that belong to the logged-in user. For example, you can use a `WHERE` clause to filter by the `user_id` column.

# By following these steps, you can enforce data isolation and ensure that each user can only access their own data.