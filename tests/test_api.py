import unittest
import falcon
from falcon import testing
from unittest.mock import MagicMock, patch
from api.api import CandleResource


class TestCandleResource(unittest.TestCase):

    def setUp(self):
        self.app = testing.TestClient(falcon.API())

        CandleResource.binance_handler = MagicMock()
        CandleResource.indicator_calculator = MagicMock()
        CandleResource.db_manager = MagicMock()

    @patch('api.api.CandleResource.CRYPTO_PAIRS', ['ETHUSDT'])
    @patch('api.api.CandleResource.TIMEFRAME', ['1h'])
    @patch('api.api.CandleResource.INDICATOR', ['EMA'])
    def test_on_get(self):
        env = testing.create_environ(path='/candles',
                                     query_string='symbol=ETHUSDT&timeframe=1h&indicator=EMA&period=5&candle_number=1')
        req = falcon.Request(env)

        resp = falcon.Response()


        CandleResource().on_get(req, resp)

        self.assertEqual(resp.status, '200 OK')


if __name__ == '__main__':
    unittest.main()
