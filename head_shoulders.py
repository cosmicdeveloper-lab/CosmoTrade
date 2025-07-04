import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


def head_shoulders(df, price_col='close', order=3, head_margin=0.01, eps_shoulders=0.05, eps_lows=0.01):
    """
    Detect Head and Shoulders patterns in a time series DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing price data. Must include 'timestamp', 'symbol', and 'timeframe' columns.
        price_col (str): The column in the DataFrame that contains price data to analyze (e.g., 'close', 'high').
        order (int): The number of points on each side to use for local minima/maxima detection (used by scipy's argrelextrema).
                     Higher values make detection stricter and reduce false positives but may miss subtle patterns.
        head_margin (float): Minimum required relative difference between the head and each shoulder.
                             E.g., 0.01 means the head must be at least 1% higher than both shoulders.
        eps_shoulders (float): Maximum allowed relative difference between left and right shoulders.
                               E.g., 0.05 allows shoulders to differ up to 5%.
        eps_lows (float): Maximum allowed relative standard deviation (std / mean) among the four key low points.
                          Used to ensure the lows forming the neckline are nearly equal.

    Returns:
        dict: A dictionary mapping the head price of each detected pattern to a string like
              "BTC hsp pattern in 1d", indicating the symbol and timeframe where the pattern was found.
    """
    df = df.copy()
    results = {}
    grouped = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in grouped:
        group = group.sort_values("timestamp").reset_index(drop=True)
        prices = group[price_col].values

        # Detect local minima and maxima
        local_max_idx = argrelextrema(prices, np.greater_equal, order=order)[0]
        local_min_idx = argrelextrema(prices, np.less_equal, order=order)[0]

        # Combine and sort extrema
        extrema_idx = np.sort(np.concatenate((local_max_idx, local_min_idx)))
        extrema_points = group.iloc[extrema_idx].reset_index()

        patterns = []

        for i in range(len(extrema_points) - 6):
            segment = extrema_points.iloc[i:i + 7]
            y = segment[price_col].values
            x = segment['index'].values

            # Check pattern type: Low-High-Low-High-Low-High-Low
            pattern = ['min', 'max', 'min', 'max', 'min', 'max', 'min']
            actual_pattern = [
                'min' if extrema_points.iloc[i + j]['index'] in local_min_idx else 'max'
                for j in range(7)
            ]
            if actual_pattern != pattern:
                continue

            # Assign labels
            P1, LS, T1, H, T2, RS, P7 = y
            idxs = x

            # Check if head > both shoulders
            if not ((H - LS) / H > head_margin and (H - RS) / H > head_margin):
                continue

            # Shoulders similar
            if abs(LS - RS) / max(LS, RS) > eps_shoulders:
                continue

            # All lows almost equal
            lows = [P1, T1, T2, P7]
            if np.std(lows) / np.mean(lows) > eps_lows:
                continue

            patterns.append({
                'indexes': idxs,
                'prices': y,
                'LS': LS,
                'H': H,
                'RS': RS,
                'lows_std': np.std(lows),
            })

            for p in patterns:
                results[p['H']] = f'head&shoulders pattern for {symbol} with timeframe {timeframe}'

    return results

