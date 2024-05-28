from data.politicians import CapitolTrades
from data.mongo import Client

# from broker import degiro

# mongo = Client()
# print(mongo.portfolio)
trades = CapitolTrades()
print(trades.get_committee("slet"))
# tr = trades.latest_trades()
# politcian = tr[1]._politicianId
# t = trades.get_all_politician_trades(politcian)
