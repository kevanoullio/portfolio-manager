-- Create database schema for the application

-- Create table for users
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT
);

-- Create table for investment type data
CREATE TABLE IF NOT EXISTS investment_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Create table for portfolio data
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    transaction_date TEXT NOT NULL,
    account TEXT,
    investment_type TEXT NOT NULL,
    symbol TEXT,
    quantity INT,
    avg_price DECIMAL(10, 2),
    total DECIMAL(10, 2),
    currency TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (investment_type) REFERENCES investment_type (type)
);



-- Create table for imported scripts
CREATE TABLE IF NOT EXISTS imported_script (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    script_path TEXT,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Add more tables as needed for other user-specific data

-- Create any additional tables for non-user-specific data

-- Create indices or other constraints as needed

-- Add more table definitions and constraints as required

-- Optionally, add sample data for testing purposes
-- INSERT INTO user (username, password_hash) VALUES ('user1', 'hashed_password1');
-- INSERT INTO user_data (user_id, data_column1, data_column2) VALUES (1, 'value1', 123);
