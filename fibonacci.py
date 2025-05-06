def get_fibo(df):
    df['fibo_618'] = df['low'] + (df['high'] - df['low']) * 0.618

    fibo_result = {}
    groups = df.groupby(['symbol', 'timeframe'])

    for (symbol, timeframe), group in groups:
        group = group.sort_values(by='timestamp').reset_index(drop=True)
        fibo = group['fibo_618'].iloc[-1]
        price = group['close'].iloc[-1]

        if abs(fibo - price) < 0.01:
            fibo_result[symbol] = f'Strong potential zone for {symbol} in timeframe {timeframe}'
    return fibo_result
