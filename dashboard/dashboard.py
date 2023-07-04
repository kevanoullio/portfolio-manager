# Purpose: Dashboard class for managing the user interface.

# Standard Libraries

# Third-party Libraries

# Local Modules
from authentication.account import Account


# Class Definitions
class Dashboard:
    def __init__(self, database):
        self.logged_in = False

    def login_menu(self) -> int:
        print("\nWelcome to 'Portfolio Manager'!")
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        print("\nPlease enter your choice: ", end="")
        choice = input()
        # Check if the input is valid
        while not choice.isdigit() or int(choice) < 0 or int(choice) > 2:
            print("Invalid input. Please try again: ", end="")
            choice = input()
        return int(choice)

    def main_menu(self) -> int:
        print("\nWelcome to 'Portfolio Manager'!")
        print("1. Manage Portfolio")
        print("2. Run A Query")
        print("3. Portfolio Analysis")
        print("4. Trading Strategies")
        print("5. Automation")
        print("6. Reports")
        print("7. Export")
        print("8. Settings")
        print("9. Log out")
        print("0. Exit")
        print("\nPlease enter your choice: ", end="")
        choice = input()
        # Check if the input is valid
        while not choice.isdigit() or int(choice) < 0 or int(choice) > 9:
            print("Invalid input. Please try again: ", end="")
            choice = input()
        return int(choice)

    def run(self):
        while True:
            if not self.logged_in:
                choice = self.login_menu()
                if choice == 1:
                    # Code for creating an account
                    print("Creating an account...")
                    self.logged_in = True
                elif choice == 2:
                    # Code for logging into an account
                    print("Logging into an account...")
                    self.logged_in = True
                else:
                    # Exit the program
                    break
            else:
                choice = self.main_menu()
                if choice == 1:
                    # Code for managing portfolio
                    print("Managing portfolio...")
                elif choice == 2:
                    # Code for running a query
                    print("Running a query...")
                elif choice == 3:
                    # Code for portfolio analysis
                    print("Performing portfolio analysis...")
                elif choice == 4:
                    # Code for trading strategies
                    print("Using trading strategies...")
                elif choice == 5:
                    # Code for automation
                    print("Automation...")
                elif choice == 6:
                    # Code for reports
                    print("Generating reports...")
                elif choice == 7:
                    # Code for export
                    print("Exporting data...")
                elif choice == 8:
                    # Code for settings
                    print("Managing settings...")
                elif choice == 9:
                    # Code for logging out
                    print("Logging out...")
                    self.logged_in = False
                else:
                    # Exit the program
                    break


if __name__ == "__main__":
    dashboard = Dashboard("db_file_test.db")
    dashboard.run()
