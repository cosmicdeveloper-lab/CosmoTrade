import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from Ichimoku_cloud import ichimoku_signal


class TestIchimokuSignal(unittest.TestCase):

    @patch('Ichimoku_cloud.IchimokuIndicator')
    def test_exit_from_above(self, MockIchimokuIndicator):
        # Mock Ichimoku lines for "exit from above"
        mock_ichimoku = MagicMock()
        mock_ichimoku.ichimoku_conversion_line.return_value = pd.Series([1.969] * 60)
        mock_ichimoku.ichimoku_base_line.return_value = pd.Series([1.969] * 60)
        mock_ichimoku.ichimoku_a.return_value = pd.Series([1.94] * 60)
        mock_ichimoku.ichimoku_b.return_value = pd.Series([1.95] * 60)
        MockIchimokuIndicator.return_value = mock_ichimoku

        data = {
            'high': [1.969] * 60,
            'low': [1.8] * 60,
            'close': [1.969] * 60,  # Price very close to span_b
            'symbol': ['ABC'] * 60,
            'timeframe': ['1h'] * 60,
            'timestamp': pd.date_range("2023-01-01", periods=60, freq='H')
        }
        df = pd.DataFrame(data)
        result = ichimoku_signal(df)

        self.assertTrue(any("Exit from above" in v for v in result.values()))

    @patch('Ichimoku_cloud.IchimokuIndicator')
    def test_exit_from_below(self, MockIchimokuIndicator):
        # Mock Ichimoku lines for "exit from below"
        mock_ichimoku = MagicMock()
        mock_ichimoku.ichimoku_conversion_line.return_value = pd.Series([1] * 60)
        mock_ichimoku.ichimoku_base_line.return_value = pd.Series([1] * 60)
        mock_ichimoku.ichimoku_a.return_value = pd.Series([4] * 60)
        mock_ichimoku.ichimoku_b.return_value = pd.Series([2] * 60)
        MockIchimokuIndicator.return_value = mock_ichimoku

        data = {
            'high': [1.999] * 60,
            'low': [2] * 60,
            'close': [1.99999] * 60,
            'symbol': ['XYZ'] * 60,
            'timeframe': ['1h'] * 60,
            'timestamp': pd.date_range("2023-01-01", periods=60, freq='H')
        }
        df = pd.DataFrame(data)
        result = ichimoku_signal(df)
        print(result)

        self.assertTrue(any("Exit from below" in v for v in result.values()))


if __name__ == '__main__':
    unittest.main()
