import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from moving_average import sma_cross


class TestSMACross(unittest.TestCase):
    @patch('moving_average.SMAIndicator')
    def test_sma_cross_bullish(self, MockSMA):
        def make_mock(return_value):
            m = MagicMock()
            m.sma_indicator.return_value = pd.Series([return_value] * 100)
            return m

        MockSMA.side_effect = [
            make_mock(10.002),  # SMA7
            make_mock(10.001),  # SMA25
            make_mock(10.000),  # SMA99
        ]

        # Create a dummy DataFrame
        data = {
            'symbol': ['BTC'] * 100,
            'timeframe': ['1h'] * 100,
            'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
            'close': [100 + i for i in range(100)]
        }
        df = pd.DataFrame(data)

        result = sma_cross(df)
        self.assertTrue(any("Bullish cross" for _, message in result.items()))

    @patch('moving_average.SMAIndicator')
    def test_sma_cross_bearish(self, MockSMA):
        def make_mock(return_value):
            m = MagicMock()
            m.sma_indicator.return_value = pd.Series([return_value] * 100)
            return m

        MockSMA.side_effect = [
            make_mock(10.000),  # SMA7
            make_mock(10.001),  # SMA25
            make_mock(10.002),  # SMA99
        ]
        # rest of tests...

        data = {
            'symbol': ['ETH'] * 100,
            'timeframe': ['1h'] * 100,
            'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='H'),
            'close': [200 + i for i in range(100)]
        }
        df = pd.DataFrame(data)

        result = sma_cross(df)
        self.assertTrue(any("Bearish cross" for _, message in result.items()))


if __name__ == '__main__':
    unittest.main()
