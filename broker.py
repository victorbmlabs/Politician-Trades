from degiro_connector.trading.api import API
from degiro_connector.trading.models.trading_pb2 import Credentials
from dotenv import load_dotenv
import os

load_dotenv()
DEGIRO_USERNAME = os.getenv("DEGIRO_USERNAME")
DEGIRO_PASSWORD = os.getenv("DEGIRO_PASSWORD")
DEGIRO_INT_ACCOUNT = os.getenv("DEGIRO_INT_ACCOUNT")
DEGIRO_USER_TOKEN = os.getenv("DEGIRO_USER_TOKEN")

degiro = API(
    Credentials(
        username=DEGIRO_USERNAME,
        password=DEGIRO_PASSWORD,
        int_account=DEGIRO_INT_ACCOUNT,
    )
)
degiro.connect()
