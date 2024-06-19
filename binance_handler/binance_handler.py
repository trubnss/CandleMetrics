import requests
import os
from binance.client import Client
from dotenv import load_dotenv


class BinanceAPIHandler:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        self.client = Client(api_key, api_secret)

    def receive_candles(self, symbol, interval, limit=100):
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

    def download_candles(self, symbol, interval, limit=100):
        # download_candles нужен если использовать библиотеку binance-api
        candles = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)

        formatted_candles = [
            {
                "timestamp": int(candle[0]),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
            }
            for candle in candles
        ]

        return formatted_candles
