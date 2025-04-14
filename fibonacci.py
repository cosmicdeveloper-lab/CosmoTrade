def get_fibo(df):
     df['fibo'] = df['high'] - (df['high'] - df['low']) * 0.618
     fibo_result = {}
     groups = df.groupby(['symbol', 'timeframe'])

     for (symbol, timeframe), group in groups:
        group = group.sort_values(by='timestamp').reset_index(drop=True)
        fibo = group['fibo'].iloc[-1]
        price = group['close'].iloc[-1]

        if fibo == price:
            fibo_result[symbol] = f'{symbol} is crossing 0.618 in timeframe {timeframe}'
     return fibo_result
