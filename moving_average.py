from ta.trend import SMAIndicator


def sma_cross(df):
    df['SMA9'] = SMAIndicator(close='close', window=9)
    df['SMA25'] = SMAIndicator(close='close', window=25)
    df['SMA99'] = SMAIndicator(close='close', window=99)

    sma_result = {}
    grouped = df.groupby(['symbol', 'timeframe'])
    for (symbol, timeframe), group in grouped:
        group = group.sort_values("timestamp").reset_index(drop=True)

        sma9 = group['SMA9'].iloc[-1]
        sma25 = group['SMA25'].iloc[-1]
        sma99 = group['SMA99'].iloc[-1]

        if sma9 == sma25 and sma9 == sma99 and sma25 == sma99:
            sma_result[symbol] = f'There is a cross on {symbol} with timeframe {timeframe}'

    return sma_result
