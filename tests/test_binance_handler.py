import unittest

from unittest.mock import patch
from binance_handler.binance_handler import BinanceAPIHandler


class TestBinanceAPIHandler(unittest.TestCase):

    @patch('binance_handler.binance_handler.requests.get')
    def test_receive_candles(self, mock_get):
        sample_response = [
            [
                1620000000000, "100.0", "110.0", "90.0", "105.0", "500",
                1620003600000, "25000.0", 200, "250.0", "1200.0", "0"
            ],
            [
                1620003600000, "105.0", "115.0", "95.0", "110.0", "600",
                1620007200000, "30000.0", 300, "300.0", "1500.0", "0"
            ],
        ]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_response

        api_handler = BinanceAPIHandler()
        symbol = "BTCUSDT"
        interval = "1h"
        limit = 2

        candles = api_handler.receive_candles(symbol, interval, limit)

        expected_candles = [
            {
                "timestamp": 1620000000000,
                "open": 100.0,
                "high": 110.0,
                "low": 90.0,
                "close": 105.0,
            },
            {
                "timestamp": 1620003600000,
                "open": 105.0,
                "high": 115.0,
                "low": 95.0,
                "close": 110.0,
            },
        ]

        self.assertEqual(candles, expected_candles)


if __name__ == '__main__':
    unittest.main()
