import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

# Import the functions to test
from rsi_prz_hangman import is_hanging_man, rsi_prz_hangman


class TestRSIPrzHangman(unittest.TestCase):

    def setUp(self):
        # Minimal setup for shared DataFrame, only used for no-signal test
        dates = pd.date_range(start='2023-01-01', periods=200, freq='H')
        self.df = pd.DataFrame({
            'timestamp': dates,
            'symbol': ['BTC'] * 200,
            'timeframe': ['1h'] * 200,
            'open': np.random.uniform(10000, 11000, 200),
            'high': np.random.uniform(11000, 12000, 200),
            'low': np.random.uniform(9000, 10000, 200),
            'close': np.random.uniform(10000, 11000, 200),
            'volume': np.random.uniform(100, 1000, 200)
        })
        self.df['RSI'] = RSIIndicator(self.df['close'], window=14).rsi()
        self.df['SMA50'] = SMAIndicator(self.df['close'], window=50).sma_indicator()
        self.df['SMA200'] = SMAIndicator(self.df['close'], window=200).sma_indicator()

    def test_rsi_prz_hangman_bullish(self):
        # Create controlled DataFrame for bullish case
        dates = pd.date_range(start='2023-01-01', periods=200, freq='H')
        bullish_df = pd.DataFrame({
            'timestamp': dates,
            'symbol': ['BTC'] * 200,
            'timeframe': ['1h'] * 200,
            'volume': [500] * 200
        })

        # Set close prices to create strong upward trend (RSI > 70)
        base_prices = np.full(186, 10000.0)  # Flat prices before the trend
        trend_prices = np.linspace(10000, 14000, 14)  # Steep upward trend for RSI
        bullish_df['close'] = np.concatenate([base_prices, trend_prices])
        bullish_df['high'] = bullish_df['close'] + 100
        bullish_df['low'] = bullish_df['close'] - 100
        bullish_df['open'] = bullish_df['close'] - 10

        # Set hanging man candle at index -2, near the high (Fibonacci 0.0% level)

        bullish_df.iloc[-2, bullish_df.columns.get_loc('high')] = 13962
        bullish_df.iloc[-2, bullish_df.columns.get_loc('open')] = 13953
        bullish_df.iloc[-2, bullish_df.columns.get_loc('close')] = 13960
        bullish_df.iloc[-2, bullish_df.columns.get_loc('low')] = 13938

        # Set SMA50 > SMA200 for bullish trend
        bullish_df['SMA50'] = SMAIndicator(bullish_df['close'], window=50).sma_indicator()
        bullish_df['SMA200'] = bullish_df['SMA50'] - 100

        # Verify RSI
        rsi = RSIIndicator(bullish_df['close'], window=14).rsi().iloc[-1]
        # print(f"Bullish RSI: {rsi}")  # Debug output

        results = rsi_prz_hangman(bullish_df)
        self.assertTrue(any('Sell' in result for result in results.values()),
                        "Should detect sell signal in bullish trend")

    def test_rsi_prz_hangman_bearish(self):
        # Create controlled DataFrame for bearish case
        dates = pd.date_range(start='2023-01-01', periods=200, freq='H')
        bearish_df = pd.DataFrame({
            'timestamp': dates,
            'symbol': ['BTC'] * 200,
            'timeframe': ['1h'] * 200,
            'volume': [500] * 200
        })

        # Set close prices to create strong downward trend (RSI < 30)
        base_prices = np.full(186, 12000.0)  # Flat prices before the trend
        trend_prices = np.linspace(12000, 8000, 14)  # Steep downward trend for RSI
        bearish_df['close'] = np.concatenate([base_prices, trend_prices])
        bearish_df['high'] = bearish_df['close'] + 100
        bearish_df['low'] = bearish_df['close'] - 100
        bearish_df['open'] = bearish_df['close'] + 10

        # Set hanging man candle at index -2, near the low (Fibonacci 0.0% level)
        bearish_df.iloc[-2, bearish_df.columns.get_loc('low')] = 8000
        bearish_df.iloc[-2, bearish_df.columns.get_loc('open')] = 8090
        bearish_df.iloc[-2, bearish_df.columns.get_loc('close')] = 8095
        bearish_df.iloc[-2, bearish_df.columns.get_loc('high')] = 8096

        # Set SMA50 < SMA200 for bearish trend
        bearish_df['SMA50'] = SMAIndicator(bearish_df['close'], window=50).sma_indicator()
        bearish_df['SMA200'] = bearish_df['SMA50'] + 100

        # Verify RSI
        rsi = RSIIndicator(bearish_df['close'], window=14).rsi().iloc[-1]
        print(f"Bearish RSI: {rsi}")  # Debug output

        results = rsi_prz_hangman(bearish_df)
        self.assertTrue(any('Buy' in result for result in results.values()),
                        "Should detect buy signal in bearish trend")


if __name__ == '__main__':
    unittest.main()
