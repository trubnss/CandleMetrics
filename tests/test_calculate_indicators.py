import unittest

from calculate_indicators.calculate_indicators import IndicatorCalculator


class TestIndicatorCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = IndicatorCalculator()

    def test_calculate_ema(self):
        pass

    def test_calculate_rsi(self):
        pass

    def test_invalid_indicator(self):
        pass


if __name__ == "__main__":
    unittest.main()
