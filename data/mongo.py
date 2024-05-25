from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from typing import TypedDict
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"), server_api=ServerApi("1"))
database = client["Congress"]

buy_orders = client.buys
sell_orders = client.sales
