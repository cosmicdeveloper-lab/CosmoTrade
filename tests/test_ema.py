import unittest
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ema import ema_cross  # Adjust this import path as needed


class TestEMACross(unittest.TestCase):
    def setUp(self):
        # Create a mock DataFrame that will force EMA50 and EMA200 to be very close
        total_rows = 300
        flat_price = 150.0
        self.df = pd.DataFrame({
            'symbol': ['AAPL'] * total_rows,
            'timeframe': ['1h'] * total_rows,
            'timestamp': pd.date_range(start='2023-01-01', periods=total_rows, freq='H'),
            'close': np.array([100.0] * 50 + [200.0] * 50 + [150.0] * 200)
        })

    def test_ema_cross_detected(self):
        result = ema_cross(self.df)
        # There should be at least one cross detected at the end
        self.assertTrue(len(result) > 0, "No EMA cross detected when expected")
        for k, v in result.items():
            self.assertIn("EMA cross on AAPL with TimeFrame 1h", v)


if __name__ == '__main__':
    unittest.main()
