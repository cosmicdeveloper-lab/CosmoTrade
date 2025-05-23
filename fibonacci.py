def get_fibo(df):
    """
    This function returns a result when price is crossing the 0.618 fibonacci
    """
    df['fibo_618'] = df['low'] + (df['high'] - df['low']) * 0.618

    # A dictionary to store the results
    fibo_result = {}
    groups = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in groups:
        group = group.sort_values(by='timestamp').reset_index(drop=True)

        fibo = group['fibo_618'].iloc[-1]
        price = group['close'].iloc[-1]
        timestamp = group['timestamp'].iloc[-1]

        if abs(fibo - price) < 0.01:
            fibo_result[timestamp.item()] = f'{symbol} with Timeframe {timeframe} Strong potential zone'

    return fibo_result
