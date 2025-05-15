from ta.trend import IchimokuIndicator


def relative_difference(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def ichimoku_signal(df):
    """
    This function return a result when conversion line,base line and price are eighter
    exiting from above the ichimoku cloud or from the bottom
    """
    ichimoku = IchimokuIndicator(
        high=df['high'],
        low=df['low'],
        window1=9,
        window2=26,
        window3=52
    )

    # Calculate each of the Ichimoku lines:
    df['Conversion_Line'] = ichimoku.ichimoku_conversion_line()
    df['Base_Line'] = ichimoku.ichimoku_base_line()
    df['Leading_Span_A'] = ichimoku.ichimoku_a()
    df['Leading_Span_B'] = ichimoku.ichimoku_b()

    # The Lagging Span (Chikou Span) is usually the close price shifted backwards (lagging) by 26 periods.
    df['Lagging_Span'] = df['close'].shift(-26)

    # A dictionary to store the results
    ichimoku_results = {}
    grouped = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in grouped:
        group = group.sort_values('timestamp').reset_index(drop=True)

        # Retrieve the elements that we need for the signal logic
        conv = group['Conversion_Line'].iloc[-1]
        base = group['Base_Line'].iloc[-1]
        span_a = group['Leading_Span_A'].iloc[-27]
        span_b = group['Leading_Span_B'].iloc[-27]
        lagging = group['Lagging_Span'].iloc[-27]
        span_a_lagging = group['Leading_Span_A'].iloc[-52]
        span_b_lagging = group['Leading_Span_B'].iloc[-52]
        price = group['high'].iloc[-1]
        timestamp = group['timestamp'].iloc[-1]
        # To check if price crossing the leading_span_b
        pb = relative_difference(price, span_b)

        # Bullish logic
        conv_bullish = conv > span_a and conv > span_b
        base_bullish = base > span_a and base > span_b
        price_bullish = price > span_a and price > span_b
        lagging_bullish = lagging > span_a_lagging and lagging > span_b_lagging
        distance_bullish = pb < 0.01

        # Bearish logic
        conv_bearish = conv < span_a and conv < span_b
        base_bearish = base < span_a and base < span_b
        price_bearish = price < span_a and price < span_b
        lagging_bearish = lagging < span_a_lagging and lagging < span_b_lagging
        near_cloud = pb < 0.01

        if conv_bullish and base_bullish and price_bullish and lagging_bullish and distance_bullish:
            ichimoku_results[timestamp] = f'{symbol} with Timeframe {timeframe} Exit from above'

        elif conv_bearish and base_bearish and price_bearish and lagging_bearish and near_cloud:
            ichimoku_results[timestamp] = f'{symbol} with Timeframe {timeframe} Exit from below'

    return ichimoku_results
