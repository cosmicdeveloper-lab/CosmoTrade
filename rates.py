import csv
import pandas as pd
import ccxt

# Load coin pairs from the CSV file
with open('symbols/top_30_coins.csv', mode='r') as file:
    reader = csv.reader(file)
    TOP_30_COINS = [row[0] for row in reader]


# Get [timestamp, open, high, low, close, volume]
def get_all_rates(symbols, timeframe=None):
    exchange = ccxt.coinex()
    frames = []
    for s in symbols:
        for t in timeframe:
            rates = exchange.fetch_ohlcv(s, timeframe=t, limit=100)
            frame = pd.DataFrame(rates, columns=["timestamp", "open", "high", "low", "close", "volume"])
            frame["symbol"] = s  # adding a column to indicate which coin it belongs to
            frame['timeframe'] = t
            frames.append(frame)
    return pd.concat(frames, ignore_index=True)
