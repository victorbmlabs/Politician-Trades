from data.politicians import CapitolTrades

# from broker import degiro

trades = CapitolTrades()
tr = trades.latest_trades()
trades.get_all_politician_trades(tr[0])
