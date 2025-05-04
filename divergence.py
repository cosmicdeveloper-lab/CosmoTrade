from ta.momentum import RSIIndicator
from ta.trend import MACD


def find_divergence(df):
    # Calculate RSI based line
    df["RSI"] = RSIIndicator(df["close"], window=14).rsi()

    # Calculate the MACD
    macd = MACD(df["close"], window_slow=26, window_fast=12, window_sign=9)
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    df["MACD_hist"] = df["MACD"] - df["MACD_signal"]

    divergence_results = {}  # A dictionary to store divergence signals per coin
    grouped = df.groupby(["symbol", "timeframe"])

    for (symbol, timeframe), group in grouped:
        # Ensure data is sorted by timestamp for each coin
        group = group.sort_values("timestamp").reset_index(drop=True)

        # MACD divergence detection
        group["positive_macd"] = group["MACD_hist"] > 0
        group["macd_trend_change"] = group["positive_macd"] != group["positive_macd"].shift()
        macd_changes = group.index[group["macd_trend_change"]].tolist()

        # Get one left to the end segment
        left_segment = group.loc[macd_changes[-2]:macd_changes[-1], "MACD_hist"]

        # Defining the segments
        try:
            s1 = group.loc[macd_changes[-4]:macd_changes[-3]]
            s2 = group.loc[macd_changes[-2]:macd_changes[-1]]
        except IndexError:
            continue

        # Getting the highest-high or the lowest-low of two left to the end segments
        divergence = None
        if (left_segment.iloc[:-1] > 0).all():
            macd1 = s1["MACD_hist"].max()
            macd2 = s2["MACD_hist"].max()
            price1 = s1["high"].max()
            price2 = s2["high"].max()
            rsi1 = s1["RSI"].max()
            rsi2 = s2["RSI"].max()
        else:
            macd1 = s1["MACD_hist"].min()
            macd2 = s2["MACD_hist"].min()
            price1 = s1["high"].min()
            price2 = s2["high"].min()
            rsi1 = s1["RSI"].min()
            rsi2 = s2["RSI"].min()

        if price1 > price2 and macd2 > macd1 and rsi2 > rsi1:
            divergence = f"{symbol} with TimeFrame {timeframe} Bullish divergence"
        elif price2 > price1 and macd1 > macd2 and rsi1 > rsi2:
            divergence = f"{symbol} with TimeFrame {timeframe} Bearish divergence"

        if divergence:
            divergence_results[symbol] = divergence

    return divergence_results
