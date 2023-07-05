# PROMPT:
# can you provide code to fetch the CAD/USD pairing from the internet using yfinance library in a python script? I'd eventually like to store daily open/close/high/low prices in an SQL table, and I'd like to make a script that automatically gets up to date information every week on Sunday at midnight. Can you explain the most efficient and best way to do this and provide me the code?

##########
# Vicuna #
##########


# To fetch historical data for the CAD/USD pairing using the yfinance library and store it in an SQL table, you can use the following Python script. To automate the process, we'll use the schedule library to run the script every week on Sunday at midnight.


# pip install yfinance sqlite3 schedule
# Here's a sample script to get you started:


import yfinance as yf
import sqlite3
import schedule
import time

def get_historical_data(symbol):
    data = yf.download(symbol, start='2000-01-01', end='2023-04-17')
    data['Close'] = data['Adj Close']
    data.reset_index(inplace=True)
    return data[['Date', 'Open', 'High', 'Low', 'Close']]

def save_to_db(data):
    conn = sqlite3.connect('historical_data.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS historical_data
                      (date TEXT, open_price REAL, high_price REAL, low_price REAL, close_price REAL)''')

    for row in data:
        cursor.execute("INSERT INTO historical_data (date, open_price, high_price, low_price, close_price) VALUES (?, ?, ?, ?, ?)", row)
        conn.commit()

    conn.close()

def update_prices():
    symbol = "CAD=USD"
    data = get_historical_data(symbol)
    save_to_db(data)

schedule.every().sunday.at("midnight").do(update_prices)

# Run the scheduler immediately
update_prices()

while True:
    time.sleep(60 * 60 * 24)  # Sleep for 24 hours
    update_prices()
    break

# This script uses the yfinance library to fetch historical data for the CAD/USD pairing. It stores the data in an SQLite database and runs automatically every week on Sunday at midnight using the schedule library.
# Please note that this is just a starting point, and you may need to adjust the code to handle errors, edge cases, or additional features.


# ####################
# # ChatGPT-3.5turbo #
# ####################

# # Certainly! To fetch the CAD/USD pairing from the internet using the yfinance library in a Python script, you can follow these steps:

# # Install the required libraries:
# # pip install yfinance
# # pip install pandas
# # pip install sqlite3

# import yfinance as yf
# import pandas as pd
# import sqlite3
# from datetime import datetime

# # Define a function to fetch the data:
# def fetch_data():
#     ticker = "CADUSD=X"  # Ticker symbol for CAD/USD pairing on Yahoo Finance
#     data = yf.download(ticker, start="YYYY-MM-DD", end="YYYY-MM-DD")  # Replace with the desired date range
    
#     # Extract the required columns from the fetched data
#     data = data[['Open', 'Close', 'High', 'Low']]
    
#     return data

# # Create a function to store the data in an SQL table:
# def store_data(data):
#     conn = sqlite3.connect('forex_data.db')  # Replace with the name of your SQLite database file
#     c = conn.cursor()
    
#     # Create the table if it doesn't exist
#     c.execute('''CREATE TABLE IF NOT EXISTS forex_data
#                  (date TEXT, open REAL, close REAL, high REAL, low REAL)''')
    
#     # Insert the data into the table
#     date = datetime.now().strftime('%Y-%m-%d')
#     for index, row in data.iterrows():
#         c.execute("INSERT INTO forex_data VALUES (?, ?, ?, ?, ?)",
#                   (date, row['Open'], row['Close'], row['High'], row['Low']))
    
#     conn.commit()
#     conn.close()

# # Schedule the script to run every week on Sunday at midnight using a task scheduler or cron job.
# # Call the functions to fetch and store the data:

# data = fetch_data()
# store_data(data)

# # Remember to replace the date range with the desired range, modify the database name and table structure as per your requirements.
# # Note: Make sure to review and comply with the terms of service of the data provider, in this case, Yahoo Finance.



# #############
# # ChatGPT-3 #
# #############

# # Certainly! To fetch the CAD/USD pairing using the yfinance library in Python, you can use the following code:

# import yfinance as yf

# def fetch_currency_data():
#     ticker = yf.Ticker("CADUSD=X")
#     data = ticker.history(period='1d')
#     return data

# currency_data = fetch_currency_data()
# print(currency_data)

# # This code uses the yfinance library to fetch the historical data for the CAD/USD pairing. It retrieves the daily historical data by using the history function with the period parameter set to '1d'. The fetched data is stored in the data variable.
# # To store the daily open/close/high/low prices in an SQL table, you'll need to establish a connection to your SQL database and execute the appropriate SQL commands. Here's an example using the sqlite3 module for a SQLite database:

# import sqlite3

# def create_currency_table():
#     conn = sqlite3.connect("currency.db")
#     cursor = conn.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS currency (
#                         date TEXT,
#                         open REAL,
#                         high REAL,
#                         low REAL,
#                         close REAL
#                       )''')
#     conn.commit()
#     conn.close()

# def insert_currency_data(data):
#     conn = sqlite3.connect("currency.db")
#     cursor = conn.cursor()
#     for index, row in data.iterrows():
#         cursor.execute("INSERT INTO currency VALUES (?, ?, ?, ?, ?)",
#                        (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close']))
#     conn.commit()
#     conn.close()

# # Fetch currency data
# currency_data = fetch_currency_data()

# # Create the currency table if it doesn't exist
# create_currency_table()

# # Insert the currency data into the table
# insert_currency_data(currency_data)

# print("Currency data inserted successfully.")

# # In the code above, the create_currency_table function creates an "currency" table if it doesn't already exist in the SQLite database. The insert_currency_data function inserts the fetched currency data into the table.
# # To automate the process to run every week on Sunday at midnight, you can use a scheduling library like schedule. Here's an example:

# import schedule
# import time

# def fetch_and_store_currency_data():
#     currency_data = fetch_currency_data()
#     create_currency_table()
#     insert_currency_data(currency_data)
#     print("Currency data inserted successfully.")

# # Schedule the job to run every Sunday at midnight
# schedule.every().sunday.at("00:00").do(fetch_and_store_currency_data)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

# # In this code, the fetch_and_store_currency_data function fetches the currency data, creates the table if needed, and inserts the data into the table. The schedule.every().sunday.at("00:00").do(fetch_and_store_currency_data) line schedules the job to run every Sunday at midnight. The loop at the end keeps the script running and continuously checks for scheduled jobs to execute.
# # Make sure to install the required libraries if you haven't already:

# # pip install yfinance
# # pip install sqlite3
# # pip install schedule

# # Remember to adjust the code to fit your specific SQL database setup and requirements.






# ########
# # Bing #
# ########

# # Yes, you can use the yfinance library to fetch the CAD/USD pairing from the internet in a Python script. Here’s an example of how you can do this:
# import yfinance as yf

# # Define the ticker symbol
# tickerSymbol = 'CAD=X'

# # Get data on this ticker
# tickerData = yf.Ticker(tickerSymbol)

# # Get the historical prices for this ticker
# tickerDf = tickerData.history(period='1d', start='2010-1-1', end='2020-1-25')

# # See your data
# print(tickerDf)

# # This code will fetch the historical prices for the CAD/USD pairing from 2010-01-01 to 2020-01-25. You can adjust the start and end parameters to specify the date range you want to fetch data for.
# # To store the data in an SQL table, you can use a Python library such as pymysql or psycopg2 to connect to your SQL database and execute SQL commands to insert the data into a table. Here’s an example of how you can do this using pymysql:

# import pymysql

# # Connect to the database
# connection = pymysql.connect(host='hostname',
#                              user='username',
#                              password='password',
#                              db='database_name')

# try:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `table_name` (`date`, `open`, `high`, `low`, `close`) VALUES (%s, %s, %s, %s, %s)"
#         for index, row in tickerDf.iterrows():
#             cursor.execute(sql, (index.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close']))

#     # Connection is not autocommit by default. So you must commit to save your changes.
#     connection.commit()
# finally:
#     connection.close()

# # This code will insert the data from the tickerDf DataFrame into a table named table_name in your SQL database. You’ll need to update the host, user, password, and db parameters with the correct values for your SQL database.
# # To automatically run your script every week on Sunday at midnight, you can use a task scheduler such as cron (on Linux or macOS) or Task Scheduler (on Windows). For example, on Linux or macOS, you can use a cron job like this:

# 0 0 * * 0 /usr/bin/python3 /path/to/your/script.py

# # This cron job will run your script every Sunday at midnight. You’ll need to update the path to your Python interpreter (/usr/bin/python3) and the path to your script (/path/to/your/script.py) with the correct values for your system.
# # I hope this helps! Let me know if you have any questions or if there’s anything else I can help with.

