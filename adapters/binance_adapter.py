import requests


class BinanceAPIHandler:
    def receive_candles(self, symbol: str, interval: str, limit: int = 100) -> list:
        """
        Получает свечи (ценовые данные) для заданного символа и интервала времени с помощью API Binance.

        :param symbol: Торговая пара, например 'BTCUSDT'.
        :param interval: Интервал времени для свечей, например '1h', '1d'.
        :param limit: Количество свечей для получения, по умолчанию 100.
        :return: Список словарей, каждый из которых представляет одну свечу.
        """
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }
        response = requests.get(url, params=params)
        data = response.json()

        candles = [
            {
                "timestamp": int(kline[0]),
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
            }
            for kline in data
        ]

        return candles
