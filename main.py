from data.politicians import CapitolTrades
from data.mongo import Client
import json

# from broker import degiro

# mongo = Client()
# print(mongo.portfolio)
trades = CapitolTrades()
committees = trades.get_committee(["slet", "hshm", "hsju"])
# tr = trades.latest_trades()
# politcian = tr[1]._politicianId
# t = trades.get_all_politician_trades(politcian)
