import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
from bollingersi import bollinger_bands


class TestBollingerBands(unittest.TestCase):

    def generate_mock_data(self, signal_type='bullish'):
        """
        Generates mock DataFrame simulating Bollinger + RSI bullish or bearish condition.
        """
        timestamps = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(30)]
        base_data = {
            'symbol': ['BTC'] * 30,
            'timeframe': ['1h'] * 30,
            'timestamp': timestamps,
            'close': [100 + i for i in range(30)],
            'high': [110 + i for i in range(30)],
            'low': [90 - i for i in range(30)]
        }
        df = pd.DataFrame(base_data)

        if signal_type == 'bullish':
            df.loc[29, 'low'] = 49.6  # Close to lower band
        else:  # bearish
            df.loc[29, 'high'] = 151  # Close to upper band

        return df

    @patch('bollingersi.RSIIndicator')
    @patch('bollingersi.BollingerBands')
    def test_bullish_signal(self, mock_bb, mock_rsi):
        df = self.generate_mock_data('bullish')

        mock_bb_instance = MagicMock()
        mock_bb_instance.bollinger_hband.return_value = [150] * 30
        mock_bb_instance.bollinger_lband.return_value = [50] * 30
        mock_bb.return_value = mock_bb_instance

        mock_rsi_instance = MagicMock()
        mock_rsi_instance.rsi.return_value = [25] * 30
        mock_rsi.return_value = mock_rsi_instance

        result = bollinger_bands(df)
        self.assertTrue(any('Bullish' in v for v in result.values()))

    @patch('bollingersi.RSIIndicator')
    @patch('bollingersi.BollingerBands')
    def test_bearish_signal(self, mock_bb, mock_rsi):
        df = self.generate_mock_data('bearish')

        mock_bb_instance = MagicMock()
        mock_bb_instance.bollinger_hband.return_value = [150] * 30
        mock_bb_instance.bollinger_lband.return_value = [50] * 30
        mock_bb.return_value = mock_bb_instance

        mock_rsi_instance = MagicMock()
        mock_rsi_instance.rsi.return_value = [75] * 30
        mock_rsi.return_value = mock_rsi_instance

        result = bollinger_bands(df)
        self.assertTrue(any('Bearish' in v for v in result.values()))


if __name__ == '__main__':
    unittest.main()
