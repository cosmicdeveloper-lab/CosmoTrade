import csv
import pandas as pd
import ccxt
from dotenv import load_dotenv
import os

# Load coin pairs from the CSV file
with open('symbols/coins.csv', mode='r') as file:
    reader = csv.reader(file)
    TOP_30_COINS = [row[0] for row in reader]


# Get [timestamp, open, high, low, close, volume]
def get_all_rates(symbols, timeframe=None):
    load_dotenv()
    exchange = os.getenv('EXCHANGE')

    if exchange in ccxt.exchanges:
        exchange_class = getattr(ccxt, exchange)
        exchange = exchange_class()
        print(f'Using exchange: {exchange}')
    else:
        print(f'Exchange {exchange} not supported by CCXT.')

    frames = []
    for s in symbols:
        for t in timeframe:
            rates = exchange.fetch_ohlcv(s, timeframe=t, limit=100)
            frame = pd.DataFrame(rates, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            frame['symbol'] = s  # adding a column to indicate which coin it belongs to
            frame['timeframe'] = t
            frames.append(frame)
    return pd.concat(frames, ignore_index=True)
