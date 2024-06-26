from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from dotenv import load_dotenv
from type import Trade
import os

load_dotenv()
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")
MONGODB_PORTFOLIO_DOCUMENT_ID = os.getenv("MONGODB_PORTFOLIO_DOCUMENT_ID")


class Client:

    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING, server_api=ServerApi("1"))
        self.database = self.client["Congress"]
        self.buy_orders = self.database.buys
        self.sell_orders = self.database.sales

    def add_purchase(trade: Trade):
        """Add a buy transaction to MongoDB"""
        pass

    def add_sale(trade: Trade):
        """Add a sale transaction to MongoDB"""
        pass

    @property
    def portfolio(self):
        """Get portfolio data from MongoDB document"""
        return self.database.portfolio.find_one(
            {"_id": ObjectId(MONGODB_PORTFOLIO_DOCUMENT_ID)}
        )
