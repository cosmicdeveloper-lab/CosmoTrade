def calculate_profit(entry, close, strategy):
    try:
        entry = float(entry)
        close = float(close)
    except (ValueError, TypeError):
        return 0.0  # or raise, or return None if you want to signal an error

    if strategy.upper() == 'BUY':
        return ((close - entry) / entry) * 100
    elif strategy.upper() == 'SELL':
        return ((entry - close) / entry) * 100
    else:
        return 0.0  # Unknown strategy
