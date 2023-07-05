
# Design Overview

**Dashboard**

1) Login and User Authentication:
    - Login to your email service provider of choice, enter username via input() and password via "from getpass import getpass"
    - Allow option to save login credentials securely (encrypted) in "user" table in the database
    - Allow logged in user to delete credentials from the table

2) Data Extraction and Management:
    - Extract raw data from email folder line by line (only clean data once entire email is extracted)
    - Use standard libraries like `import email`, `import imaplib`, and `from html.parser import HTMLParser` via a Python script.

2) Data Cleaning and Preparation:
    - Clean up data for each email separately once extraction of entire email is complete, all using Python only
    - Once each individual email is cleaned, store it into SQL database directly using `import sqlite3`
    - Either Python alone (no libraries) or `pandas` for data cleaning operations such as handling missing values, and transforming data types if necessary.

3) Data Storage:
    - Establish a connection to an SQLite3 database using the `sqlite3` module in Python.
    - Store cleaned data directly in an SQLite3 .db database file.
    - Create appropriate table structures with primary keys and relationships for efficient data storage.
    - Use the sqlite3 module in Python to establish a connection with the database and execute SQL statements for creating tables and inserting data.
    - Use parameterized SQL statements to prevent SQL injection vulnerabilities.
    - Insert each individual email entry separately and do so immediately after both extracting and cleaning

4) Efficient Data Organization:
    - Define appropriate table structures, primary keys (uid), and relationships to ensure efficient data retrieval and analysis.
    - Consider the use of normalization techniques to eliminate data redundancy and improve query performance.

5) Track the Last Processed Email:
    - Implement a mechanism to keep track of the last processed email.
    - Store the metadata and/or unique identifier of the last processed email (uid for sure, and email and folder all 3 primary key?).

6) Check for Duplicates:
    - Consider using a combination of unique constraints, primary keys (uid for sure, and email and folder all 3 primary key?), and SQL queries to check for duplicates before inserting new records.
    - Query the database with a SELECT statement using the unique identifier(s) and check if any matching records are returned.
    - When you clean and normalize the data, you can preserve this unique identifier and use it as the primary key in the SQLite database. This way, when you add new data to the database, you can use the INSERT OR IGNORE or INSERT OR REPLACE commands to prevent duplicates based on the primary key.

7) Securely Insert Non-Duplicate Records:
    - Use SQL statements such as INSERT INTO ... WHERE NOT EXISTS to insert only new and unique data.
    - Implement error handling mechanisms to handle any exceptions that may occur during the insertion process.
    - Log and appropriately display error messages to facilitate debugging and issue resolution.

8) Automation and Integration:
    - Automate the email extraction, data cleaning, and database update processes using Python scripts.
    - Utilize scheduling libraries like `schedule` or system-level tools like cron to schedule regular script execution.
    - Configure the scheduled scripts to run at appropriate intervals for timely data updates.
    - User can define the automation intervals from the dashboard

9) User Interface/Dashboard:
    - Design and implement a user-friendly interface using Python.
    - TODO Utilize frameworks like Flask, Django, Dash, Streamlit, or Panel to build an interactive and responsive dashboard.
    - Provide menu options and interactive components to allow users to execute queries, view data, and access various functionalities.

10) Data Analysis and Visualization:
    - Utilize SQL queries on the SQLite3 database to perform data analysis.
    - Utilize libraries like `numpy`, `pandas`, and `matplotlib` for efficient data manipulation and visualization, generating plots, charts, and graphs.
    - Consider using a data visualization tool such as Tableau or Power BI to create interactive dashboards and reports that summarize the key insights from your data.

11) Pre-Calculated Data for Analysis:
    - Consider creating additional tables or fields in the database to store aggregated or summarized data for specific time periods (monthly, yearly, etc.) or any other relevant categorization.
    - You can create tables that store summary statistics, such as monthly or yearly returns, trade counts, profit/loss, etc.
    - These pre-calculated tables can help speed up analysis and make it easier to query and visualize specific subsets of data.

12) Advanced Visualizations and Statistical Analysis:
    - Use numpy and pandas for advanced statistical analysis of the S&P 500, NASDAQ 100, and other indexes, as well as comparisons with your portfolio data.
    - Utilize `numpy` and `pandas` for advanced statistical analysis, including comparisons between relevant indexes (SPX, NDX, etc) and your portfolio.
    - ???Utilize advanced visualization libraries like Plotly or Seaborn to create interactive and informative charts, plots, and dashboards???

13) Trading Strategies and Performance Analysis:
    - Define trading strategies or analysis techniques and apply them to the cleaned data to derive meaningful insights.
    - Generate charts, plots, and graphs to visualize the data and analyze the results of trading strategies.

14) Filtering, Sorting, and Customized Reports:
    - Enhance the dashboard with features for data filtering, sorting, and generating customized reports.

15) Export Data:
    - Allow user the option to export any of the data visualizations, customized reports, or any combination of filtered or unfiltered or sorted or unsorted data.
    - Support export to various file formats such as TXT, CSV, PNG, DOC, PDF, etc.


# Organization of Code 

1. Main Dashboard Script:
   - Create a main script `dashboard.py`, that acts as the entry point for your application.
   - This script will handle the main menu and user interaction.
   - Based on the user's selection, it will call functions or modules responsible for specific tasks.

2. Modular Approach:
   - Break down your application into separate modules, each responsible for a specific functionality.
   - For example, `login.py`, `database.py`, `import.py`, `automation.py`, `data_analysis.py`, `trading_strategies.py`, `reports.py`, etc.
   - Each module can contain the necessary functions, classes, or methods to handle the related tasks.


3. Importing and Calling Modules:
   - Import the required modules within your main `dashboard.py` script.
   - Use the module names directly when importing, without specifying subdirectories.
   - For example, `import login`, `import database`, `import automation`, etc.

4. Shared Utilities Functions:
   - You can also create a separate module for shared utilities or helper functions that are used across different modules.
   - If you have reusable helper utils functions, you can keep them in a separate `utils.py` script.
   - Import the helper functions into the modules that require them.

5. Additional Considerations:
   - If certain functionalities are better suited to be implemented in other languages, you can create separate scripts or modules for those tasks and integrate them into your Python code using appropriate techniques like subprocess or APIs.

6. Directory Structure:

    ```
    Portfolio-Manager/
    |-- portfolio-manager.py
    |-- config.py
    |-- dashboard/
    |   |--__init__.py
    |   |-- dashboard.py
    |-- authentication/
    |   |--__init__.py
    |   |-- account.py
    |-- database/
    |   |--__init__.py
    |   |-- database.db
    |   |-- database.py
    |   |-- schema.sql
    |-- import/
    |   |--__init__.py
    |   |-- import_csv.py
    |   |-- import_email_account.py
    |   |-- import_market_data.py
    |-- automation/
    |   |--__init__.py
    |   |-- automate.py
    |-- data_analysis/
    |   |--__init__.py
    |   |-- portfolio_analysis.py
    |-- trading_strategies/
    |   |--__init__.py
    |   |-- trading_strategies.py
    |-- reports/
    |   |--__init__.py
    |   |-- generate_reports.py
    |-- export/
    |   |--__init__.py
    |   |-- export_options.py
    |   |-- format_data.py
    |   |-- export_data.py
    |-- user_data/
    |   |-- portfolio.db

    POSSIBLE ADDITIONS
    |-- templates/
    |   |-- index.html
    |   |-- login.html
    |   |-- extraction.html
    |   |-- automation.html
    |   |-- analysis.html
    |   |-- strategies.html
    |   |-- reports.html
    |   |-- export.html
    |-- static/
    |   |-- css/
    |   |   |-- style.css
    |   |-- js/
    |   |   |-- main.js
    ```

Explanation of the directory structure:

- `dashboard.py`: The main entry point of your application. It handles routing and serves as the starting point for the dashboard.
- `config.py`: Configuration file to store any application-specific settings or variables.
- `database/`: A folder dedicated to all database-related operations.
  - `database.db`: Contains all data for program (user data, login, etc)
  - `database.py`: Contains functions and classes to interact with the SQLite3 database.
  - `schema.sql`: SQL script defining the table structures and relationships for the database.
- `authentication/`: Contains modules related to user authentication.
  - `account.py`: Handles the login functionality and user authentication.
- `import/`: Contains modules for extracting data from email folders.
  - `import.py`: Implements functions to import data from emails using the specified libraries.
- `automation/`: Handles automation tasks related to email extraction, data cleaning, and database updates.
  - `automate.py`: Contains functions and scripts for automating the processes.
- `data_analysis/`: Includes modules for performing data analysis.
  - `analysis.py`: Implements functions for querying and analyzing data from the SQLite3 database.
- `trading_strategies/`: Contains modules for implementing and testing trading strategies.
  - `strategies.py`: Implements various trading strategies and analysis techniques.
- `reports/`: Handles the generation of customized reports.
  - `generate_reports.py`: Implements functions to generate reports based on specified criteria.
- `export/`: Contains modules for exporting data and visualizations.
  - `export_data.py`: Implements functions to export data and visualizations in different formats.
- `user_data/`: Contains all user specific portfolio data
    |   |-- `portfolio.db`: Main database file for all user data
Possible Additions
- `templates/`: Contains HTML templates for the dashboard.
- `static/`: Includes static assets such as CSS and JavaScript files.
  - `css/`: Contains CSS files for styling the dashboard.
  - `js/`: Contains JavaScript files for any client-side functionality.

This directory structure separates different modules based on the main menu options, making it easier to maintain and navigate through the codebase. Each module can be developed independently and imported as needed within the main application.


# Config File

The config.py file is commonly used to store configuration settings for a Python application. It provides a centralized location to define and access various parameters or settings that can be used throughout the application. This includes things like database connection details, API keys, file paths, logging configurations, and other environment-specific variables.

Using a .py file for configuration has several advantages. It allows you to define variables as Python objects, which means you can use Python syntax and leverage the flexibility of the language. Additionally, you can easily import and access these configuration settings from other modules in your application. This makes it convenient to change settings in one place without modifying multiple files.

Here's an example of a `config.py` file that includes different types of configuration settings:

```python
# Database connection details
DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'mydatabase'
DB_USER = 'myuser'
DB_PASSWORD = 'mypassword'

# API keys
API_KEY_1 = 'myapikey1'
API_KEY_2 = 'myapikey2'

# File paths
DATA_FILE_PATH = '/path/to/data/file.csv'
LOG_FILE_PATH = '/path/to/log/file.log'

# Logging configurations
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'

# Environment-specific variables
if ENVIRONMENT == 'development':
    DEBUG = True
    DATABASE_URL = 'dev-database-url'
else:
    DEBUG = False
    DATABASE_URL = 'prod-database-url'
```


# Schema File

The schema.sql file is typically used to define the database schema, which includes the structure, relationships, and constraints of the database tables. It is written in SQL (Structured Query Language) and contains the necessary SQL statements to create tables, define columns, set primary keys, establish foreign key relationships, and enforce constraints like unique values or not null requirements. The schema file is executed during the setup or initialization process of the database to create the required tables and their structures.

Certainly! Here's an example of a `schema.sql` file that defines the database schema using SQL statements:

```sql
-- Create the "users" table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the "orders" table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the "products" table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);
```

In this example, we have three tables: "users", "orders", and "products". The "users" table has a unique username and email, while the "orders" table has a foreign key relationship with the "users" table.

To execute the `schema.sql` file and create the required tables and their structures, you can use a database management tool or execute the SQL statements programmatically. Here's an example of how you can execute the schema file using Python and the `sqlite3` module:

```python
import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# Read the schema file
with open('schema.sql', 'r') as file:
    schema = file.read()

# Execute the schema SQL statements
cursor.executescript(schema)

# Commit the changes and close the connection
conn.commit()
conn.close()
```

In this example, we use the `executescript()` method of the `cursor` object to execute the SQL statements from the `schema.sql` file. The `commit()` method is used to save the changes, and the `close()` method is used to close the connection to the database.

You can place this code in your setup or initialization process to create the required tables and their structures in the database. Make sure to adjust the database connection details (`mydatabase.db`) and the file path of the `schema.sql` file according to your specific setup.


# Template Folder

The templates/ folder contains HTML templates for the dashboard. HTML templates are used to define the structure and layout of web pages. They provide a way to separate the presentation logic from the actual content of the page. In the context of a dashboard, HTML templates are used to create the visual representation of the different pages or views in the dashboard application. Each HTML file represents a specific page or component of the dashboard and can include placeholders or template tags to dynamically insert data from the server-side code. This allows you to generate dynamic HTML pages that can be rendered with different data based on user interactions or backend calculations.


# Possible New Dashboard Design

Here are some examples of interfaces or dashboards that can be built using Python frameworks like Flask, Django, or Dash:

1) Flask:
    - Flask is a lightweight web framework that can be used to build web interfaces and dashboards.
    - With Flask, you can create custom HTML templates and serve them dynamically based on data from your Python code.
    - Flask-Admin is an extension that provides an interface to manage your data models and create administrative dashboards.

2) Django:
    - Django is a robust web framework that includes many built-in features for building web applications and dashboards.
    - Django provides an admin interface out-of-the-box, which allows you to manage your application's data models and create customized dashboards for data visualization and manipulation.
    - You can also leverage Django's templating engine to create dynamic web interfaces.

3) Dash:
    - Dash is a Python framework specifically designed for building interactive web-based dashboards.
    - Dash allows you to create rich, interactive dashboards with data visualization components like charts, graphs, and tables.
    - It offers a reactive programming model, allowing you to update the dashboard in response to user interactions or data changes.

4) Streamlit:
    - Streamlit is a popular Python framework for building interactive data science applications and dashboards.
    - It provides a simple and intuitive API for creating interactive web interfaces directly from Python scripts.
    - Streamlit allows you to quickly prototype and deploy data-driven applications with minimal boilerplate code.

5) Panel:
    - Panel is a Python library that works with multiple frameworks, including Flask and Django, to create interactive dashboards and applications.
    - Panel provides a wide range of interactive widgets and visualization components that can be easily integrated into web interfaces.
    - It supports data visualization libraries like Matplotlib, Bokeh, Plotly, and more.

These frameworks offer different features and cater to different use cases. Choose the one that aligns with your project requirements and preferences in terms of simplicity, flexibility, and the specific functionality you need for your interface or dashboard.


