from ta.trend import EMAIndicator
import pandas as pd

pd.options.mode.copy_on_write = True


def relative_difference(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def ema_cross(df):
    """
    this function return a result when moving averages exponential cross 50 200
    """

    # Calculate the moving averages
    df['EMA50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['EMA200'] = EMAIndicator(close=df['close'], window=200).ema_indicator()

    # A dictionary to store the results
    ema_result = {}
    grouped = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in grouped:
        group = group.sort_values("timestamp").reset_index(drop=True)

        ema50 = group['EMA50'].iloc[-1]
        ema200 = group['EMA200'].iloc[-1]
        difference = relative_difference(ema50, ema200)

        if difference < 0.01:
            signal_id = float(f'{difference:.3f}')
            ema_result[signal_id] = f'EMA cross on {symbol} with TimeFrame {timeframe} '

    return ema_result
