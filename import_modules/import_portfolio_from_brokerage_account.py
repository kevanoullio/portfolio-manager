# Purpose: Import portfolio from brokerage account using SnapTradeClient class from the snaptrade_client module.

# Standard Libraries

# Third-party Libraries
from snaptrade_client import SnapTradeClient

# Local modules imported for Type Checking purposes only

# Configure logging
import logging


# Initialize SnapTrade Client
client = SnapTradeClient(
    client_id="your_client_id",
    consumer_key="your_consumer_key"
)

# Step 1: Redirect user to authorization URL
auth_url = client.get_authorization_url(
    redirect_uri="https://yourapp.com/callback"
)
print(f"Visit this URL to connect your brokerage: {auth_url}")

# Step 2: After user grants permission, handle callback
authorization_code = input("Enter the authorization code from the callback URL: ")
tokens = client.exchange_code_for_tokens(authorization_code)

# Step 3: Access user data
portfolio = client.get_portfolio_data(access_token=tokens['access_token'])
print(portfolio)
