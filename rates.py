import csv
import pandas as pd
import ccxt
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# Load coin pairs from the CSV file
with open('symbols/coins.csv', mode='r') as file:
    reader = csv.reader(file)
    TOP_30_COINS = [row[0] for row in reader]


# Get [timestamp, open, high, low, close, volume]
def get_all_rates(symbols=None, timeframe=None):
    if timeframe is None and symbols is None:
        timeframe = ['2h', '4h', '1d']
        symbols = TOP_30_COINS

    load_dotenv()
    exchange = os.getenv('EXCHANGE')
    if exchange in ccxt.exchanges:
        exchange_class = getattr(ccxt, exchange)
        exchange = exchange_class()
        logger.info(f'Using exchange: {exchange}')
    else:
        logger.error(f'Exchange {exchange} not supported by CCXT.')

    frames = []
    for s in symbols:
        for t in timeframe:
            rates = exchange.fetch_ohlcv(s, timeframe=t, limit=200)
            frame = pd.DataFrame(rates, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            frame['symbol'] = s  # adding a column to indicate which coin it belongs to
            frame['timeframe'] = t
            frames.append(frame)
    return pd.concat(frames, ignore_index=True)
