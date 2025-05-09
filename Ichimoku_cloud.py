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
        price = group['close'].iloc[-1]
        timestamp = group['timestamp'].iloc[-1]
        pb = relative_difference(price, span_b)

        if all(x > span_b and x > span_a for x in [conv, base, price, lagging]) and (0.05 > pb):
            ichimoku_results[timestamp] = f'{symbol} with Timeframe {timeframe} Exit from above'

        elif all(x < span_b and x < span_a for x in [conv, base, price, lagging]) and (0.05 > pb):
            ichimoku_results[timestamp] = f'{symbol} with Timeframe {timeframe} Exit from below'

    return ichimoku_results
