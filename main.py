from data.politicians import CapitolTrades
from data.mongo import Client
from data.finance import calculate_bollinger_bands, calculate_rsi, calculate_adx

# from broker import degiro

# mongo = Client()
# print(mongo.portfolio)
# trades = CapitolTrades()
# committees = trades.get_committee(["slet", "hshm", "hsju"])
# tr = trades.latest_trades()
# politcian = tr[1]._politicianId
# t = trades.get_all_politician_trades(politcian)


from data.markets import get_stock_by_ticker

stock = get_stock_by_ticker("NVDA")
obv = calculate_adx(stock)
print(obv)
