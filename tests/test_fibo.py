import unittest
import pandas as pd
from datetime import datetime, timedelta
from fibonacci import get_fibo


class TestGetFibo(unittest.TestCase):

    def test_fibo_zone_triggered(self):
        """
        Test that get_fibo detects when price crosses the 0.618 Fibonacci level.
        """
        timestamps = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(10)]
        high = 110
        low = 100
        fibo_618 = low + (high - low) * 0.618  # This will be 106.18

        data = {
            'symbol': ['BTC'] * 10,
            'timeframe': ['1h'] * 10,
            'timestamp': timestamps,
            'high': [high] * 10,
            'low': [low] * 10,
            'close': [105] * 9 + [106.18]  # last close is at fibo level
        }
        df = pd.DataFrame(data)

        result = get_fibo(df)

        self.assertTrue(any("Strong potential zone" in v for v in result.values()))
        self.assertIn(timestamps[-1], result)


if __name__ == '__main__':
    unittest.main()
