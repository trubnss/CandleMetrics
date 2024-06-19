import unittest
from unittest.mock import patch, MagicMock
import falcon
from falcon import testing
import json

from api.api import app


class TestCandleResource(testing.TestCase):
    def setUp(self):
        super().setUp()
        self.app = app

    @patch("binance_handler.binance_handler.BinanceAPIHandler.receive_candles")
    @patch("db_handler.db_handler.DatabaseManager.store_candles")
    @patch("db_handler.db_handler.DatabaseManager.get_candles")
    @patch(
        "calculate_indicators.calculate_indicators.IndicatorCalculator.calculate_indicator"
    )
    def test_on_get(
        self,
        mock_calculate_indicator,
        mock_get_candles,
        mock_store_candles,
        mock_receive_candles,
    ):
        mock_receive_candles.return_value = [
            {
                "timestamp": 1625239200000,
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
            },
            # добавьте еще свечи, если нужно
        ]
        mock_get_candles.return_value = MagicMock()
        mock_calculate_indicator.return_value = mock_get_candles.return_value

        params = {
            "symbol": "ETHUSDT",
            "timeframe": "1d",
            "indicator": "EMA",
            "period": "3",
            "candle_number": "0",
        }
        result = self.simulate_get("/candles", params=params)

        self.assertEqual(result.status, falcon.HTTP_200)
        response_data = json.loads(result.text)
        self.assertIn("timestamp", response_data)
        self.assertIn("open", response_data)
        self.assertIn("high", response_data)
        self.assertIn("low", response_data)
        self.assertIn("close", response_data)
        self.assertIn("indicator", response_data)

    def test_invalid_crypto_pair(self):
        params = {
            "symbol": "INVALIDPAIR",
            "timeframe": "1d",
            "indicator": "EMA",
            "period": "3",
            "candle_number": "0",
        }
        result = self.simulate_get("/candles", params=params)

        self.assertEqual(result.status, falcon.HTTP_400)
        response_data = json.loads(result.text)
        self.assertEqual(response_data["title"], "Неверная криптопара")

    def test_missing_params(self):
        params = {
            "symbol": "ETHUSDT",
            "timeframe": "1d",
            "indicator": "EMA",
            "period": None,
            "candle_number": "0",
        }
        result = self.simulate_get("/candles", params=params)

        self.assertEqual(result.status, falcon.HTTP_400)
        response_data = json.loads(result.text)
        self.assertTrue(response_data["title"].startswith("Отсутствуют параметры"))

    def test_invalid_candle_number(self):
        params = {
            "symbol": "ETHUSDT",
            "timeframe": "1d",
            "indicator": "EMA",
            "period": "3",
            "candle_number": "invalid",
        }
        result = self.simulate_get("/candles", params=params)

        self.assertEqual(result.status, falcon.HTTP_400)
        response_data = json.loads(result.text)
        self.assertEqual(response_data["title"], "Некорректные параметры")

    @patch("binance_handler.binance_handler.BinanceAPIHandler.receive_candles")
    @patch("db_handler.db_handler.DatabaseManager.store_candles")
    @patch("db_handler.db_handler.DatabaseManager.get_candles")
    @patch(
        "calculate_indicators.calculate_indicators.IndicatorCalculator.calculate_indicator"
    )
    def test_candle_number_out_of_bounds(
        self,
        mock_calculate_indicator,
        mock_get_candles,
        mock_store_candles,
        mock_receive_candles,
    ):
        mock_receive_candles.return_value = [
            {
                "timestamp": 1625239200000,
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
            },
            # добавьте еще свечи, если нужно
        ]
        mock_get_candles.return_value = MagicMock()
        mock_calculate_indicator.return_value = mock_get_candles.return_value

        params = {
            "symbol": "ETHUSDT",
            "timeframe": "1d",
            "indicator": "EMA",
            "period": "3",
            "candle_number": "100",  # Номер свечи выходит за пределы
        }
        result = self.simulate_get("/candles", params=params)

        self.assertEqual(result.status, falcon.HTTP_400)
        response_data = json.loads(result.text)
        self.assertEqual(response_data["title"], "Недопустимый номер свечи")


if __name__ == "__main__":
    unittest.main()
