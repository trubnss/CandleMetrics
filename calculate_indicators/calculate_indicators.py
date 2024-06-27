import pandas as pd
import pandas_ta

from ports.db_port import DatabasePort


class IndicatorCalculator:
    def __init__(self, database_port:DatabasePort):
        self.database_port = database_port

    def calculate_indicator(self, data_frame: pd.DataFrame, indicator: str, period: int) -> pd.DataFrame:
        """
        Вычисляет указанный индикатор для переданных данных.

        :param data_frame: DataFrame, содержащий данные свечей.
        :param indicator: Название индикатора, который необходимо вычислить (например, 'EMA', 'RSI').
        :param period: Период, используемый для вычисления индикатора.
        :return: DataFrame с добавленным столбцом индикатора.
        """
        if indicator == "EMA":
            data_frame["indicator"] = pandas_ta.ema(data_frame["close"], length=period)
        elif indicator == "RSI":
            data_frame["indicator"] = pandas_ta.rsi(data_frame["close"], length=period)
        else:
            raise ValueError("Invalid indicator")

        return data_frame
