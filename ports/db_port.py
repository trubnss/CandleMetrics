import pandas as pd
from abc import ABC, abstractmethod


class DatabasePort(ABC):
    @abstractmethod
    def create_table(self, table_name: str) -> None:
        pass

    @abstractmethod
    def create_pair(self, symbol: str) -> None:
        pass

    @abstractmethod
    def store_candles(self, symbol: str, timeframe: str, candles: list) -> None:
        pass

    @abstractmethod
    def get_candles(self, symbol: str, timeframe: str) -> pd.DataFrame:
        pass