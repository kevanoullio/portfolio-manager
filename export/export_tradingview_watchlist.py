import requests
import sqlite3

class Portfolio:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def export_to_tradingview(self, api_key, api_secret):
        # Retrieve assets and sectors from database
        # self.cursor.execute("""
        #     SELECT asset.symbol, sector.name AS sector
        #     FROM asset_info asset
        #     JOIN sector sector ON asset.sector_id = sector.id
        # """)
        # Replace above with already cursor execution functions
        assets = self.cursor.fetchall()

        # Create a TradingView API session
        session = requests.Session()
        session.auth = (api_key, api_secret)

        # Create a new watchlist
        watchlist_id = session.post("(link unavailable)", json={"name": "My Owned Assets"}).json()["id"]

        # Add assets to the watchlist with sections
        for symbol, sector in assets:
            session.post(f"(link unavailable)", json={"symbol": symbol, "section": sector})

        self.conn.close()

# Example usage
portfolio = Portfolio("assets.db")
portfolio.export_to_tradingview("API_KEY", "API_SECRET")
