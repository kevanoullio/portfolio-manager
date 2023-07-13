-- Create database schema for the application

-- Create table for users
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash BLOB NOT NULL,
    created_at VARCHAR(255) DEFAULT CURRENT_TIMESTAMP
);

-- Create table for email usage
CREATE TABLE IF NOT EXISTS email_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usage VARCHAR(255) UNIQUE NOT NULL
);

-- Insert default email usage
INSERT OR IGNORE INTO email_usage (usage) VALUES ('import_email_account');
INSERT OR IGNORE INTO email_usage (usage) VALUES ('email_notification');

-- Create table for user email accounts
CREATE TABLE IF NOT EXISTS email (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    password_hash BLOB NOT NULL,
    email_usage_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (email_usage_id) REFERENCES email_usage (id)
);

-- Create table for asset class type data
CREATE TABLE IF NOT EXISTS asset_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    [type] VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    UNIQUE (user_id, [type])
);

-- Create table for portfolio data
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    account VARCHAR(255) NOT NULL,
    asset_class_id INTEGER NOT NULL,
    symbol VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    avg_price DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(63) NOT NULL,
    import_file VARCHAR(255),
    import_date VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (asset_class_id) REFERENCES asset_class (id)
);

-- Create table for data types
CREATE TABLE IF NOT EXISTS data_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Create table for imported data
CREATE TABLE IF NOT EXISTS imported_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    [name] VARCHAR(255) NOT NULL,
    data_type_id INTEGER NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    import_date VARCHAR(255) DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (data_type_id) REFERENCES data_type (id)
);



-- Add more tables as needed for other user-specific data

-- Create any additional tables for non-user-specific data

-- Create indices or other constraints as needed

-- Add more table definitions and constraints as required


-- Optionally, add sample data for testing purposes
-- INSERT INTO user (username, password_hash) VALUES ('user1', 'hashed_password1');
-- INSERT INTO user_data (user_id, data_column1, data_column2) VALUES (1, 'value1', 123);
