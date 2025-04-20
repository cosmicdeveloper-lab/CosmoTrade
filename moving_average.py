from ta.trend import SMAIndicator


def relative_difference(a, b):
    return abs(a - b) / max(abs(a), abs(b))


def sma_cross(df):
    df['SMA7'] = SMAIndicator(close=df['close'], window=7).sma_indicator()
    df['SMA25'] = SMAIndicator(close=df['close'], window=25).sma_indicator()
    df['SMA99'] = SMAIndicator(close=df['close'], window=99).sma_indicator()

    sma_result = {}
    grouped = df.groupby(['symbol', 'timeframe'])
    for (symbol, timeframe), group in grouped:
        group = group.sort_values("timestamp").reset_index(drop=True)

        sma7 = group['SMA7'].iloc[-1]
        sma25 = group['SMA25'].iloc[-1]
        sma99 = group['SMA99'].iloc[-1]

        if (1 <= relative_difference(sma7, sma25) and relative_difference(sma7, sma99)
                and relative_difference(sma25, sma99) < 1.1):
            sma_result[symbol] = f'There is a cross on {symbol} with timeframe {timeframe}'

    return sma_result
