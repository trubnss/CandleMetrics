from abc import ABC, abstractmethod


class BinancePort(ABC):
    @abstractmethod
    def receive_candles(self, symbol: str, interval: str, limit: int = 100) -> list:
        pass
