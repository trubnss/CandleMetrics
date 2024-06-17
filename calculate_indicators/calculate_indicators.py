import pandas_ta


class IndicatorCalculator:
    def calculate_indicator(self, data_frame, indicator, period):
        if indicator == "EMA":
            data_frame["indicator"] = pandas_ta.ema(data_frame["close"], length=period)
        elif indicator == "RSI":
            data_frame["indicator"] = pandas_ta.rsi(data_frame["close"], length=period)
        else:
            raise ValueError("Invalid indicator")

        return data_frame
