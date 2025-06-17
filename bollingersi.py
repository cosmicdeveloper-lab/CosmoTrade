from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator


def relative_difference(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def bollinger_bands(df):

    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close=df["close"], window=30, window_dev=2)

    # Add Bollinger Bands features
    df['bb_bbh'] = indicator_bb.bollinger_hband()
    df['bb_bbl'] = indicator_bb.bollinger_lband()

    # Calculate RSI based line
    df['RSI'] = RSIIndicator(df['close'], window=13).rsi()

    # A dictionary to store the results
    bollinger_result = {}
    grouped = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in grouped:
        # Ensure data is sorted by timestamp for each coin
        group = group.sort_values('timestamp').reset_index(drop=True)

        price_upper = group['high'].iloc[-1]
        price_lower = group['low'].iloc[-1]
        lower_band = group['bb_bbl'].iloc[-1]
        upper_band = group['bb_bbh'].iloc[-1]
        rsi = group['RSI'].iloc[-1]

        bearish_differ = relative_difference(upper_band, price_upper)
        bullish_differ = relative_difference(lower_band, price_lower)

        if bearish_differ < 0.01 and rsi > 70:
            signal_id = float(f'{rsi:.2g}')
            bollinger_result[signal_id] = f'Bearish trend on {symbol} with TimeFrame {timeframe}'
        elif bullish_differ < 0.01 and rsi < 30:
            signal_id = float(f'{rsi:.2g}')
            bollinger_result[signal_id] = f'Bullish trend on {symbol} with TimeFrame {timeframe}'

    return bollinger_result
