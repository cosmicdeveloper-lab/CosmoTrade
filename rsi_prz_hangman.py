from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
import numpy as np
from scipy.signal import argrelextrema


def is_hanging_man(df):
    open_price = df['open'].iloc[-2]
    high = df['high'].iloc[-2]
    low = df['low'].iloc[-2]
    close = df['close'].iloc[-2]

    body = abs(close - open_price)
    upper_shadow = high - max(open_price, close)
    lower_shadow = min(open_price, close) - low
    total_range = high - low

    # Criteria for hanging man
    return (
        body <= total_range * 0.3 and           # small body
        lower_shadow >= body * 2 and            # long lower shadow
        upper_shadow <= body * 0.3              # small or no upper shadow
    )


def rsi_prz_hangman(df, tolerance=0.02):
    """
        Identifies trading signals based on RSI, Fibonacci retracement levels, and Hanging Man candlestick patterns.
        This function analyzes a DataFrame containing price data to detect potential buy or sell signals for
        multiple symbols and timeframes. It uses the Relative Strength Index (RSI), Simple Moving Averages (SMA50
        and SMA200), Fibonacci retracement levels, and the Hanging Man candlestick pattern to identify trading
        opportunities in bullish or bearish trends.

        Parameters:
        -----------
        df : pandas.DataFrame
        tolerance : float, optional (default=0.02)
            The maximum allowable difference (as a fraction of the price) between the current price and a
            Fibonacci retracement level to consider it a match.

        Returns:
        --------
        dict
            A dictionary where keys are price levels (high or low prices) and values are strings describing the
            trading signal
        Notes:
        ------
        - The function uses a 14-period RSI to identify overbought (>70) or oversold (<30) conditions.
        - Fibonacci retracement levels (0.0%, 23.6%, 38.2%, 50.0%, 61.8%, 78.6%, 100.0%) are calculated
          based on the highest high and lowest low within the data.
        - A Hanging Man candlestick pattern is checked for confirmation of sell signals in bullish trends
          or buy signals in bearish trends.
        - The trend is determined by comparing SMA50 and SMA200 (SMA50 > SMA200 for bullish,
          SMA50 < SMA200 for bearish).
        - Local minima and maxima are identified using a 15-period window for peak detection.
        """

    # Calculate RSI based line
    df['RSI'] = RSIIndicator(df['close'], window=14).rsi()

    # Calculate SMA
    df['SMA50'] = SMAIndicator(df['close'], window=50).sma_indicator()
    df['SMA200'] = SMAIndicator(df['close'], window=200).sma_indicator()

    results = {}
    grouped = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in grouped:
        # Ensure data is sorted by timestamp for each coin
        group = group.sort_values('timestamp').reset_index(drop=True)

        rsi = group['RSI'].iloc[-1]

        # Find local minima and maxima
        group['Min'] = group['low'][argrelextrema(group['low'].values, np.less_equal, order=15)[0]]
        group['Max'] = group['high'][argrelextrema(group['high'].values, np.greater_equal, order=15)[0]]

        high = group['Max'].dropna().max()
        low = group['Min'].dropna().min()

        sma50 = group['SMA50'].iloc[-1]
        sma200 = group['SMA200'].iloc[-1]

        hh_hanging_man = group['high'].iloc[-2]
        ll_hanging_man = group['low'].iloc[-2]
        last_candle = group['close'].iloc[-1]

        uptrend_price = group['high'].iloc[-1]
        downtrend_price = group['low'].iloc[-1]
        diff = high - low

        if sma50 > sma200:
            bullish_levels = {
                '0.0%': high,
                '23.6%': high - (0.236 * diff),
                '38.2%': high - (0.382 * diff),
                '50.0%': high - (0.5 * diff),
                '61.8%': high - (0.618 * diff),
                '78.6%': high - (0.786 * diff),
                '100.0%': low
            }

            match = any(abs(uptrend_price - level) <= tolerance for level in bullish_levels.values())

            if rsi > 70 and is_hanging_man(group) and match and ll_hanging_man > last_candle:
                results[uptrend_price] = f'Sell for {symbol} with {timeframe}'

        if sma50 < sma200:
            bearish_levels = {
                '0.0%': low,
                '23.6%': low + (0.236 * diff),
                '38.2%': low + (0.382 * diff),
                '50.0%': low + (0.5 * diff),
                '61.8%': low + (0.618 * diff),
                '78.6%': low + (0.786 * diff),
                '100.0%': low
            }

            match = any(abs(downtrend_price - level) <= tolerance for level in bearish_levels.values())

            if rsi < 30 and is_hanging_man(group) and match and hh_hanging_man < last_candle:
                results[downtrend_price] = f'Buy for {symbol} with timeframe {timeframe}'

    return results
