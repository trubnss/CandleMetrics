import falcon
import json

from adapters.database_manager import DatabaseManager
from core.calculate_indicators import IndicatorCalculator
from ports.binance_port import BinancePort


class CandleResource:
    """
    Ресурс для работы со свечами, поддерживающий получение свечей с Binance, их хранение и расчёт индикаторов.
    """
    CRYPTO_PAIRS = [
        "ETHUSDT",
        "LTCUSDT",
        "XLMUSDT",
        "XMRUSDT",
        "XEMUSDT",
    ]

    TIMEFRAME = [
        "1d",
        "1h",
    ]

    INDICATOR = [
        "EMA",
        "RSI",
    ]

    def __init__(self, binance_handler: BinancePort, db_manager: DatabaseManager):
        self.binance_handler = binance_handler
        self.db_manager = db_manager
        self.indicator_calculator = IndicatorCalculator(self.db_manager)

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        symbol = req.get_param("symbol")
        timeframe = req.get_param("timeframe")
        indicator = req.get_param("indicator")
        period = req.get_param("period")
        candle_number = req.get_param("candle_number")

        if symbol not in self.CRYPTO_PAIRS:
            raise falcon.HTTPBadRequest(
                title="Неверная криптопара",
                description=f"Допустимые криптопары: {', '.join(self.CRYPTO_PAIRS)}",
            )

        if timeframe not in self.TIMEFRAME:
            raise falcon.HTTPBadRequest(
                title="Неверный датафрейм",
                description=f"Допустимые датафреймы: {', '.join(self.TIMEFRAME)}",
            )

        if indicator not in self.INDICATOR:
            raise falcon.HTTPBadRequest(
                title="Неверный индикатор",
                description=f"Допустимые индикаторы: {', '.join(self.TIMEFRAME)}",
            )

        if not all([symbol, timeframe, indicator, period, candle_number]):
            missing_params = [
                param
                for param, value in {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "indicator": indicator,
                    "period": period,
                    "candle_number": candle_number,
                }.items()
                if not value
            ]
            raise falcon.HTTPBadRequest(
                title=f"Отсутствуют параметры: {', '.join(missing_params)}"
            )

        try:
            candle_number = int(candle_number)
            period = int(period)
        except ValueError:
            raise falcon.HTTPBadRequest(
                title="Некорректные параметры",
                description="Параметры period и candle_number должны быть целыми числами",
            )

        candles = self.binance_handler.receive_candles(
            symbol, timeframe
        )  # Получение свечей с binance
        self.db_manager.store_candles(symbol, timeframe, candles)  # Запись свитчей в БД

        candles_from_db = self.db_manager.get_candles(symbol, timeframe)
        # Расчет индикатора
        candles_with_indicator = self.indicator_calculator.calculate_indicator(
            candles_from_db, indicator, period
        )

        try:
            result = candles_with_indicator.iloc[
                candle_number
            ].to_dict()  # Формирование ответа из dataframe в dict
        except IndexError:
            raise falcon.HTTPBadRequest(
                title="Недопустимый номер свечи",
                description="Номер свечи выходит за пределы доступных данных",
            )

        resp.text = json.dumps(result)
        resp.status = falcon.HTTP_200


def create_app(binance_handler, db_manager):
    app = falcon.App()
    candle_resource = CandleResource(binance_handler, db_manager)
    app.add_route("/candles", candle_resource)
    return app
