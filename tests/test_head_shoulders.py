import unittest
import pandas as pd
from head_shoulders import head_shoulders


class TestHeadShouldersDetection(unittest.TestCase):

    def setUp(self):
        # Simulated head and shoulders pattern
        self.df = pd.DataFrame({
            'timestamp': pd.date_range(start='2023-01-01', periods=30, freq='D'),
            'symbol': ['BTC'] * 30,
            'timeframe': ['1d'] * 30,
            'close': [
                100, 105, 102,   # Left shoulder
                120, 150, 124,   # Head
                100, 105, 102,   # Right shoulder
                102, 101, 100,   # Lows
                99,  100, 101,   # Lows continue
                102, 103, 104,   # After pattern
                105, 106, 107,
                106, 104, 102,
                100,  98,  96,
                97,  99,  100,
            ]
        })

    def test_head_and_shoulders_detection(self):
        results = head_shoulders(
            self.df,
            price_col='close',
            order=1,
            head_margin=0.005,
            eps_shoulders=0.1,
            eps_lows=0.03
        )

        # Check that pattern is detected
        self.assertTrue(any("BTC" in v for v in results.values()))
        self.assertTrue(any("1d" in v for v in results.values()))
        self.assertGreater(len(results), 0)


if __name__ == '__main__':
    unittest.main()
