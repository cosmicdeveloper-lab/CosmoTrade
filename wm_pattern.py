def relative_difference(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def zigzag(df, deviation=1, threshold=0.02):

    """
        Identifies zigzag patterns (M and W patterns) in financial price data for multiple symbols and timeframes.

        This function analyzes a DataFrame containing price data to detect pivot points based on a specified
        deviation percentage and identifies M and W patterns when consecutive pivot points
        have a relative difference below a given threshold. The analysis is performed on the last 30 closing
        prices for each symbol and timeframe group.

        Parameters:
        -----------
        df : pandas.DataFrame
        deviation : float, optional (default=1)
            The minimum percentage change (drop or rise) required to identify a pivot point.
            Expressed as a percentage (e.g., 1 for 1%).
        threshold : float, optional (default=0.02)
            The maximum relative difference between two pivot points to classify them as part of an
            M or W pattern. Expressed as a fraction (e.g., 0.02 for 2%).

        Returns:
        --------
        dict
            A dictionary where keys are pivot point prices and values are strings describing the detected
            pattern (e.g., "M pattern for {symbol} with timeframe {timeframe}" or
        """

    all_results = {}  # Collect results for all symbols

    grouped = df.groupby(['symbol', 'timeframe'])
    for (symbol, timeframe), group in grouped:

        # Ensure data is sorted by timestamp for each coin
        group = group.sort_values('timestamp').reset_index(drop=True)

        # Input data: list of closes or highs/lows
        prices = group['close'].tolist()
        last_50 = prices[-30:]

        trend = 'up'  # start uptrend
        pivot_list = []
        patterns = {}

        highest_high = last_50[0]
        lowest_low = last_50[0]

        for price in last_50:
            if trend == 'up':
                if price > highest_high:
                    highest_high = price

                drop = (highest_high - price) / highest_high * 100
                if drop >= deviation:
                    pivot_list.append(highest_high)
                    trend = 'down'
                    lowest_low = price  # reset lowest

                    if len(pivot_list) > 3:
                        if relative_difference(pivot_list[-1], pivot_list[-3]) < threshold:
                            patterns[pivot_list[-1]] = f'M pattern for {symbol} with timeframe {timeframe} M pattern'

            elif trend == 'down':
                if price < lowest_low:
                    lowest_low = price

                rise = (price - lowest_low) / lowest_low * 100
                if rise >= deviation:
                    pivot_list.append(lowest_low)
                    trend = 'up'
                    highest_high = price  # reset highest

                    if len(pivot_list) > 3:
                        if relative_difference(pivot_list[-1], pivot_list[-3]) < threshold:
                            patterns[pivot_list[-1]] = f'W pattern for {symbol} with timeframe {timeframe} '
        all_results.update(patterns)

    return all_results
