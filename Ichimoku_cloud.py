from ta.trend import IchimokuIndicator


def ichimoku_signal(df):
    ichimoku = IchimokuIndicator(
        high=df["high"],
        low=df["low"],
        window1=9,
        window2=26,
        window3=52
    )

    # Calculate each of the Ichimoku lines:
    df["Conversion_Line"] = ichimoku.ichimoku_conversion_line()
    df["Base_Line"] = ichimoku.ichimoku_base_line()
    df["Leading_Span_A"] = ichimoku.ichimoku_a()
    df["Leading_Span_B"] = ichimoku.ichimoku_b()

    # The Lagging Span (Chikou Span) is usually the close price shifted backwards (lagging) by 26 periods.
    df["Lagging_Span"] = df["close"].shift(-26)

    signals = {}
    grouped = df.groupby(["symbol", "timeframe"])

    for (symbol, timeframe), group in grouped:
        group = group.sort_values("timestamp").reset_index(drop=True)

        # Retrieve the latest values for each line for the current symbol
        conv = group['Conversion_Line'].iloc[-1]
        base = group['Base_Line'].iloc[-1]
        span_a = group['Leading_Span_A'].iloc[-1]
        span_b = group['Leading_Span_B'].iloc[-1]
        lagging = group['Lagging_Span'].iloc[-27]

        if all(x > span_a and x > span_b for x in [conv, base, lagging]):
            signals[symbol] = f'Exit from above in {symbol} in timeframe {timeframe}'
        elif all(x < span_a and x < span_b for x in [conv, base, lagging]):
            signals[symbol] = f'Exit from below in {symbol} in timeframe {timeframe}'

    return signals
