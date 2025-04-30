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
        group["bullish_macd"] = group["MACD_hist"] > 0
        group["macd_trend_change"] = group["bullish_macd"] != group["bullish_macd"].shift()
        macd_changes = group.index[group["macd_trend_change"]].tolist()

        macd_extrema = []
        for i in range(len(macd_changes) - 1):
            start, end = macd_changes[i], macd_changes[i + 1]
            segment = group.iloc[start:end]
            # Choose max if starting positive, else min
            if segment["MACD_hist"].dropna().empty: # Decide what to do if all values are NA,data may occasionally contain missing values.
                idx = None
            else:
                idx = segment["MACD_hist"].idxmax() if segment["MACD_hist"].iloc[0] > 0 else segment[
                    "MACD_hist"].idxmin()
            macd_extrema.append(idx)

        # RSI divergence detection
        group["rsi_diff"] = group["RSI"].diff()
        group["bullish_rsi"] = group["rsi_diff"] > 0
        group["rsi_trend_change"] = group["bullish_rsi"] != group["bullish_rsi"].shift()
        rsi_changes = group.index[group["rsi_trend_change"]].tolist()

        rsi_extrema = []
        for i in range(len(rsi_changes) - 1):
            start, end = rsi_changes[i], rsi_changes[i + 1]
            segment = group.iloc[start:end]
            idx = segment["RSI"].idxmax() if segment["rsi_diff"].iloc[0] > 0 else segment["RSI"].idxmin()
            rsi_extrema.append(idx)

        divergence = None
        if len(macd_extrema) >= 2 and len(rsi_extrema) >= 2:
            try:
                p1, p2 = macd_extrema[-3], macd_extrema[-1]
            except:
                continue
            price1, price2 = group["close"].iloc[p1], group["close"].iloc[p2]
            macd1, macd2 = group["MACD_hist"].iloc[p1], group["MACD_hist"].iloc[p2]
            rsi1, rsi2 = group["RSI"].iloc[p1], group["RSI"].iloc[p2]

            if price2 > price1 and macd2 < macd1 and rsi2 < rsi1:
                divergence = f"{symbol} with TimeFrame {timeframe} Bearish divergence"
            elif price2 < price1 and macd2 > macd1 and rsi2 > rsi1:
                divergence = f"{symbol} with TimeFrame {timeframe} Bullish divergence"

        if divergence:
            divergence_results[symbol] = divergence

    return divergence_results
