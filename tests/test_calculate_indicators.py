import unittest
import pandas as pd
from core.calculate_indicators import IndicatorCalculator


class TestIndicatorCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = IndicatorCalculator()

    def test_calculate_indicator_invalid_indicator(self):
        data = {
            "close": [1, 2, 3, 4, 5]
        }
        df = pd.DataFrame(data)

        with self.assertRaises(ValueError):
            self.calculator.calculate_indicator(df, "invalid_indicator", 5)


if __name__ == '__main__':
    unittest.main()
