----------------------------------------
-- DATABASE SCHEMA FOR INITIALISATION --
----------------------------------------

-- Create table for user roles
CREATE TABLE IF NOT EXISTS user_role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE (user_id, [name])
);

-- Insert default user roles
INSERT OR IGNORE INTO user_role (user_id, [name]) VALUES ('admin');
INSERT OR IGNORE INTO user_role (user_id, [name]) VALUES ('user');

-- Create table for users
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_role_id INTEGER NOT NULL,
    username VARCHAR(255) NOT NULL,
    password_hash BLOB NOT NULL,
    created_at VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_role_id) REFERENCES user_role (id),
    UNIQUE (username)
);

--------------------
-- EMAIL ACCOUNTS --
--------------------

-- Create table for email usage
CREATE TABLE IF NOT EXISTS email_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usage VARCHAR(255) NOT NULL,
    UNIQUE (usage)
);

-- Insert default email usages
INSERT OR IGNORE INTO email_usage (usage) VALUES ('import');
INSERT OR IGNORE INTO email_usage (usage) VALUES ('notification');

-- Create table for user email accounts
CREATE TABLE IF NOT EXISTS email (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_usage_id INTEGER NOT NULL,
    [address] VARCHAR(255) NOT NULL,
    password_hash BLOB,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (email_usage_id) REFERENCES email_usage (id)
);

-----------------------------
-- ASSETS AND TRANSACTIONS --
-----------------------------

-- Create table for asset class data (e.g. stock, bond, etc.)
CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Insert default asset classes
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('stock');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('bond');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('etf');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('cryptocurrency');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('mutual fund');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('option');
INSERT OR IGNORE INTO asset_class ([name]) VALUES ('other');

-- Create table for asset sector data
CREATE TABLE IF NOT EXISTS sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class_id INTEGER NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    FOREIGN KEY (asset_class_id) REFERENCES asset_class (id),
    UNIQUE (asset_class_id, [name])
);

-- Create table for asset industry data
CREATE TABLE IF NOT EXISTS industry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_id INTEGER NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    FOREIGN KEY (sector_id) REFERENCES sector (id),
    UNIQUE (sector_id, [name])
);

-- Create table for asset country data
CREATE TABLE IF NOT EXISTS country (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for asset currency data
CREATE TABLE IF NOT EXISTS currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for asset exchange data
CREATE TABLE IF NOT EXISTS exchange (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    acronym VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for asset data
CREATE TABLE IF NOT EXISTS asset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_class_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    industry_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    exchange_id INTEGER NOT NULL,
    symbol VARCHAR(255) NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    FOREIGN KEY (asset_class_id) REFERENCES asset_class (id),
    FOREIGN KEY (sector_id) REFERENCES sector (id),
    FOREIGN KEY (industry_id) REFERENCES industry (id),
    FOREIGN KEY (country_id) REFERENCES country (id),
    FOREIGN KEY (currency_id) REFERENCES currency (id),
    FOREIGN KEY (exchange_id) REFERENCES exchange (id),
    UNIQUE (exchange_id, symbol)
);

-- Create table for asset transaction types
CREATE TABLE IF NOT EXISTS transaction_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
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
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for asset account data
CREATE TABLE IF NOT EXISTS asset_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for asset transaction data
CREATE TABLE IF NOT EXISTS asset_transaction (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    transaction_type_id INTEGER NOT NULL,
    brokerage_id INTEGER NOT NULL,
    asset_account_id VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    avg_price DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    transaction_date DATE NOT NULL,
    imported_from VARCHAR(255),
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (asset_id) REFERENCES asset (id),
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_type (id),
    FOREIGN KEY (brokerage_id) REFERENCES brokerage (id),
    FOREIGN KEY (asset_account_id) REFERENCES asset_account (id)
);

------------------------
-- FOR DATA IMPORTING --
------------------------

-- Create table for data types
CREATE TABLE IF NOT EXISTS data_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    [name] VARCHAR(255) NOT NULL,
    UNIQUE ([name])
);

-- Create table for imported data
CREATE TABLE IF NOT EXISTS imported_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    data_type_id INTEGER NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    import_date VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (data_type_id) REFERENCES data_type (id)
);



-- Create indices or other constraints as needed
-- Add more table definitions and constraints as required
