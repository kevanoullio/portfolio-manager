----------------------------------------
-- DATABASE SCHEMA FOR INITIALISATION --
----------------------------------------

-- Create table for user roles
CREATE TABLE IF NOT EXISTS user_role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Insert default user roles
INSERT OR IGNORE INTO user_role ([name]) VALUES ('admin');
INSERT OR IGNORE INTO user_role ([name]) VALUES ('user');

-- Create table for users
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_role_id INTEGER NOT NULL REFERENCES user_role (id),
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash BLOB NOT NULL,
    created_at VARCHAR(255) DEFAULT CURRENT_TIMESTAMP
);

--------------------
-- EMAIL ACCOUNTS --
--------------------

-- Create table for email usage
CREATE TABLE IF NOT EXISTS email_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usage VARCHAR(255) NOT NULL UNIQUE
);

-- Insert default email usages
INSERT OR IGNORE INTO email_usage (usage) VALUES ('import');
INSERT OR IGNORE INTO email_usage (usage) VALUES ('notification');

-- Create table for user email accounts
CREATE TABLE IF NOT EXISTS email (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    email_usage_id INTEGER NOT NULL REFERENCES email_usage (id),
    [address] VARCHAR(255) NOT NULL,
    password_hash BLOB
);

-- Create table for imported email log
CREATE TABLE IF NOT EXISTS imported_email_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    email_id INTEGER NOT NULL REFERENCES email (id),
    folder_name VARCHAR(255) NOT NULL,
    last_uid INT NOT NULL,
    last_uid_updated_at VARCHAR(255) DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to ensure email_id references an email with 'import' usage
CREATE TRIGGER enforce_import_email
BEFORE INSERT ON imported_email_log
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Invalid email_id. The email must have usage type "import"')
    WHERE (SELECT usage FROM email_usage WHERE id = NEW.email_id) != 'import';
END;

-- Only keep the last 100 import email settings for a given user's email and folder combination
DELETE FROM imported_email_log
WHERE (user_id, email_id, folder_name, id) NOT IN (
    SELECT user_id, email_id, folder_name, id FROM imported_email_log
    ORDER BY id DESC
    LIMIT 10000
);

--------------------------------
-- ASSETS AND HISTORICAL DATA --
--------------------------------

-- Create table for asset class data (e.g. equity, fixed income, etc.)
CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Create table for asset sub class data (e.g. stock, bond, etc.)
CREATE TABLE IF NOT EXISTS asset_subclass (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class_id INTEGER NOT NULL REFERENCES asset_class (id),
    [name] VARCHAR(255) NOT NULL,
    UNIQUE (asset_class_id, [name])
);

-- Create table for asset sector data
CREATE TABLE IF NOT EXISTS sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class_id INTEGER NOT NULL REFERENCES asset_class (id),
    [name] VARCHAR(255) NOT NULL,
    UNIQUE (asset_class_id, [name])
);

-- Create table for asset industry data
CREATE TABLE IF NOT EXISTS industry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_id INTEGER NOT NULL REFERENCES sector (id),
    [name] VARCHAR(255) NOT NULL,
    UNIQUE (sector_id, [name])
);

-- Create table for asset country data
CREATE TABLE IF NOT EXISTS country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE,
    iso_code VARCHAR(255) NOT NULL UNIQUE
);

-- Create table for asset city data
CREATE TABLE IF NOT EXISTS city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL REFERENCES country (id),
    [name] VARCHAR(255) NOT NULL,
    UNIQUE (country_id, [name])
);

-- Create table for asset currency data
CREATE TABLE IF NOT EXISTS currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE,
    iso_code VARCHAR(255) NOT NULL UNIQUE,
    symbol NVARCHAR(10) NOT NULL
);

-- Create table for exchange data
CREATE TABLE IF NOT EXISTS exchange (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL REFERENCES country (id),
    [name] VARCHAR(255) NOT NULL UNIQUE,
    acronym VARCHAR(255) NOT NULL UNIQUE
);

-- -- Create table for exchange listing data
-- CREATE TABLE IF NOT EXISTS exchange_listing (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     exchange_id INTEGER NOT NULL REFERENCES exchange (id),
--     exchange_currency_id INTEGER NOT NULL REFERENCES currency (id),
--     symbol VARCHAR(255) NOT NULL,
--     company_name VARCHAR(255) NOT NULL,
--     UNIQUE (exchange_id, symbol)
-- );

-- Create table for asset data
CREATE TABLE IF NOT EXISTS asset_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class_id INTEGER NOT NULL REFERENCES asset_class (id),
    asset_subclass_id INTEGER NOT NULL REFERENCES asset_subclass (id),
    sector_id INTEGER NOT NULL REFERENCES sector (id),
    industry_id INTEGER NOT NULL REFERENCES industry (id),
    country_id INTEGER NOT NULL REFERENCES country (id),
    city_id VARCHAR(255) NOT NULL REFERENCES city (id),
    financial_currency_id INTEGER NOT NULL REFERENCES currency (id),
    exchange_currency_id INTEGER NOT NULL REFERENCES currency (id),
    exchange_id INTEGER NOT NULL REFERENCES exchange (id),
    symbol VARCHAR(255) NOT NULL,
    security_name VARCHAR(255) NOT NULL,
    business_summary VARCHAR(1023),
    website VARCHAR(255),
    logo_url VARCHAR(255),
    UNIQUE (exchange_id, symbol)
);

-- Create table for asset price history data
CREATE TABLE IF NOT EXISTS asset_price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL REFERENCES asset_info (id),
    [date] DATE NOT NULL,
    [open] DECIMAL(10, 2) NOT NULL,
    high DECIMAL(10, 2) NOT NULL,
    low DECIMAL(10, 2) NOT NULL,
    [close] DECIMAL(10, 2) NOT NULL,
    adj_close DECIMAL(10, 2) NOT NULL,
    volume INT NOT NULL,
    UNIQUE (asset_id, [date])
);

-- Create table for asset dividend history data
CREATE TABLE IF NOT EXISTS dividend_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL REFERENCES asset_info (id),
    [date] DATE NOT NULL,
    dividend DECIMAL(10, 2) NOT NULL,
    UNIQUE (asset_id, [date])
);

-- Create table for asset split history data
CREATE TABLE IF NOT EXISTS split_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL REFERENCES asset_info (id),
    [date] DATE NOT NULL,
    stock_split DECIMAL(10, 2) NOT NULL,
    UNIQUE (asset_id, [date])
);

------------------------
-- ASSET TRANSACTIONS --
------------------------

-- Create table for asset transaction types
CREATE TABLE IF NOT EXISTS transaction_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Insert default transaction types
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('market buy');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('market sell');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('limit buy');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('limit sell');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('stop buy');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('stop sell');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('stop limit buy');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('stop limit sell');
INSERT OR IGNORE INTO transaction_type ([name]) VALUES ('dividend');

-- Create table for brokerage data
CREATE TABLE IF NOT EXISTS brokerage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Create table for asset account data
CREATE TABLE IF NOT EXISTS asset_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Create table for asset transaction data
CREATE TABLE IF NOT EXISTS asset_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    asset_id INTEGER NOT NULL REFERENCES asset_info (id),
    transaction_type_id INTEGER NOT NULL REFERENCES transaction_type (id),
    brokerage_id INTEGER NOT NULL REFERENCES brokerage (id),
    asset_account_id VARCHAR(255) NOT NULL REFERENCES asset_account (id),
    quantity DECIMAL (10, 2) NOT NULL,
    avg_price DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    imported_from VARCHAR(255),
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

----------------
-- INDEX DATA --
----------------

-- Create table for index data
CREATE TABLE IF NOT EXISTS index_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exchange_id INTEGER NOT NULL REFERENCES exchange (id),
    [name] VARCHAR(255) NOT NULL UNIQUE,
    symbol VARCHAR(255) NOT NULL UNIQUE,
    [description] VARCHAR(1023) NOT NULL,
    website_url VARCHAR(255) NOT NULL,
    table_index INTEGER NOT NULL,
    symbol_column VARCHAR(255) NOT NULL,
    UNIQUE (exchange_id, symbol)
);

-- Create table for index holdings data
CREATE TABLE IF NOT EXISTS index_holdings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    index_id INTEGER NOT NULL REFERENCES index_info (id),
    asset_id INTEGER NOT NULL REFERENCES asset_info (id),
    UNIQUE (index_id, asset_id)
);

-- Create table for index price history data
CREATE TABLE IF NOT EXISTS index_price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    index_id INTEGER NOT NULL REFERENCES index_info (id),
    [date] DATE NOT NULL,
    [open] DECIMAL(10, 2) NOT NULL,
    high DECIMAL(10, 2) NOT NULL,
    low DECIMAL(10, 2) NOT NULL,
    [close] DECIMAL(10, 2) NOT NULL,
    adj_close DECIMAL(10, 2) NOT NULL,
    volume INT NOT NULL,
    UNIQUE (index_id, [date])
);

--------------------
-- DATA IMPORTING --
--------------------

-- Create table for data types
CREATE TABLE IF NOT EXISTS data_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL UNIQUE
);

-- Create table for imported data
CREATE TABLE IF NOT EXISTS imported_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES user (id),
    data_type_id INTEGER NOT NULL REFERENCES data_type (id),
    [name] VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    import_date VARCHAR(255) DEFAULT CURRENT_TIMESTAMP
);
