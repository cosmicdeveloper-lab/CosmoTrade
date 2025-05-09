import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
from divergence import find_divergence


class TestFindDivergence(unittest.TestCase):

    def generate_mock_data(self, trend='bullish'):
        """
        Generates a DataFrame with MACD histogram pattern and price to simulate
        bullish or bearish divergence.
        """
        timestamps = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(10)]
        df = pd.DataFrame({
            'symbol': ['BTC'] * 10,
            'timeframe': ['1h'] * 10,
            'timestamp': timestamps,
            'close': [100 + i for i in range(10)],
            'high': (
                [100, 102, 104, 106, 108, 107, 106, 105, 104, 103]
                if trend == 'bullish' else
                [110, 108, 106, 104, 102, 103, 104, 105, 106, 107]
            )
        })
        return df

    @patch('divergence.RSIIndicator')
    @patch('divergence.MACD')
    def test_bullish_divergence_detection(self, mock_macd, mock_rsi):
        df = self.generate_mock_data('bullish')

        # Mock RSI
        mock_rsi_instance = MagicMock()
        mock_rsi_instance.rsi.return_value = [30, 32, 34, 35, 37, 36, 38, 39, 40, 42]
        mock_rsi.return_value = mock_rsi_instance

        # Mock MACD
        mock_macd_instance = MagicMock()
        mock_macd_instance.macd.return_value = [1, -1, 1, -1, 1, -1, 1, -1, 2, -1]  # 9 changes
        mock_macd_instance.macd_signal.return_value = [0] * 10  # Keep signal flat to simplify

        mock_macd.return_value = mock_macd_instance

        result = find_divergence(df)
        self.assertTrue(any('Bullish divergence' in v for v in result.values()))

    @patch('divergence.RSIIndicator')
    @patch('divergence.MACD')
    def test_bearish_divergence_detection(self, mock_macd, mock_rsi):
        df = self.generate_mock_data('bearish')

        # Mock RSI
        mock_rsi_instance = MagicMock()
        mock_rsi_instance.rsi.return_value = [70, 68, 66, 64, 62, 63, 61, 60, 59, 58]
        mock_rsi.return_value = mock_rsi_instance

        # Mock MACD
        mock_macd_instance = MagicMock()
        mock_macd_instance.macd.return_value = [0.5, -0.2, 0.2, 0.1, 0.4, 0.6, -0.2, 0.1, -0.5, 0.3]
        mock_macd_instance.macd_signal.return_value = [0] * 10  # So hist = macd - signal
        mock_macd.return_value = mock_macd_instance

        result = find_divergence(df)
        self.assertTrue(any('Bearish divergence' in v for v in result.values()))


if __name__ == '__main__':
    unittest.main()
