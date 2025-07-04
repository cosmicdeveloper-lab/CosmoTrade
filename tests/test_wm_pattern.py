import unittest
import pandas as pd

from wm_pattern import relative_difference, zigzag


class TestZigzagModule(unittest.TestCase):

    def test_zigzag_detects_M_pattern(self):
        prices = [100, 105, 100, 106, 100, 107, 100]
        df = pd.DataFrame({
            'symbol':    ['SYM'] * len(prices),
            'timeframe': ['1h'] * len(prices),
            'timestamp': list(range(len(prices))),
            'close':     prices
        })

        result = zigzag(df, deviation=1, threshold=0.1)

        # after four pivots, the last low ≈ the 2nd low → M pattern at price 100
        self.assertIn(107, result)
        self.assertEqual(result[107], 'M pattern SYM with 1h')

    def test_zigzag_detects_W_pattern(self):
        prices = [100, 105, 100, 106, 100, 107, 100]
        df = pd.DataFrame({
            'symbol':    ['SYM'] * len(prices),
            'timeframe': ['1h'] * len(prices),
            'timestamp': list(range(len(prices))),
            'close':     prices
        })

        result = zigzag(df, deviation=1, threshold=0.1)

        # after four pivots, the last low ≈ the 2nd low → M pattern at price 100
        self.assertIn(100, result)
        self.assertEqual(result[100], 'W pattern SYM with 1h')


if __name__ == '__main__':
    unittest.main()
