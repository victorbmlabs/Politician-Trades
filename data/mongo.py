from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from dotenv import load_dotenv
from type import Trade
import os

load_dotenv()
CONNECTION_STRING = os.getenv("MONGODB_CONNECTION_STRING")


class Client:

    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING, server_api=ServerApi("1"))
        self.database = self.client["Congress"]
        self.buy_orders = self.database.buys
        self.sell_orders = self.database.sales

    def add_purchase(trade: Trade):
        pass

    def add_sale(trade: Trade):
        pass

    @property
    def portfolio(self):
        id = "6655b5e32840e72fc504e572"
        return self.database.portfolio.find_one({"_id": ObjectId(id)})
