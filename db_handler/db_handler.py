# import os
# import psycopg2
# import pandas as pd
#
# from dotenv import load_dotenv
#
# load_dotenv()
#
#
# class DatabaseManager:
#     def __init__(self, db_connection=None):
#         """
#         Инициализирует менеджер базы данных, создавая подключение к базе данных.
#
#         :param db_connection: Опциональное подключение к базе данных. Если не указано, создается новое подключение.
#         """
#         self.con = db_connection or psycopg2.connect(
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT"),
#             database=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD")
#
#         )
#
#     def create_table(self, table_name: str) -> None:
#         """
#         Создает таблицу для хранения данных свечей, если она не существует.
#
#         :param table_name: Название таблицы для создания.
#         """
#         cursor = self.con.cursor()
#         create_query = f"""
#         CREATE TABLE IF NOT EXISTS {table_name} (
#             id SERIAL PRIMARY KEY,
#             symbol TEXT NOT NULL,
#             open REAL NOT NULL,
#             high REAL NOT NULL,
#             low REAL NOT NULL,
#             close REAL NOT NULL,
#             timestamp BIGINT NOT NULL,
#             FOREIGN KEY (symbol) REFERENCES crypto_pair (symbol)
#         )
#         """
#         cursor.execute(create_query)
#         self.con.commit()
#
#     def create_pair(self, symbol: str) -> None:
#         """
#         Создает таблицу для хранения криптовалютных пар и добавляет указанную пару, если она не существует.
#
#         :param symbol: Символ криптовалютной пары для добавления.
#         """
#         cursor = self.con.cursor()
#         create_query = """
#         CREATE TABLE IF NOT EXISTS crypto_pair(
#             id SERIAL PRIMARY KEY,
#             symbol TEXT NOT NULL UNIQUE
#         )
#         """
#         cursor.execute(create_query)
#         cursor.execute(
#             "INSERT INTO crypto_pair (symbol) VALUES (%s) ON CONFLICT DO NOTHING", (symbol,)
#         )
#         self.con.commit()
#
#     def store_candles(self, symbol: str, timeframe: str, candles: list[dict]) -> None:
#         """
#         Сохраняет данные свечей в таблице.
#
#         :param symbol: Символ криптовалютной пары.
#         :param timeframe: Таймфрейм для свечей.
#         :param candles: Список свечей, представленных как словари с ключами 'open', 'high', 'low', 'close', 'timestamp'.
#         """
#         table_name = f"t_{timeframe}_candles"
#         self.create_pair(symbol)
#         self.create_table(table_name)
#
#         cursor = self.con.cursor()
#         insert_query = f"""
#         INSERT INTO {table_name} (
#             symbol,
#             open,
#             high,
#             low,
#             close,
#             timestamp
#         )
#         VALUES (%s, %s, %s, %s, %s, %s)
#         """
#         for candle in candles:
#             cursor.execute(
#                 insert_query,
#                 (
#                     symbol,
#                     candle["open"],
#                     candle["high"],
#                     candle["low"],
#                     candle["close"],
#                     candle["timestamp"],
#                 ),
#             )
#
#         self.con.commit()
#
#     def get_candles(self, symbol: str, timeframe: str) -> pd.DataFrame:
#         """
#         Извлекает данные свечей из таблицы.
#
#         :param symbol: Символ криптовалютной пары.
#         :param timeframe: Таймфрейм для свечей.
#         :return: Данные свечей в виде DataFrame.
#         """
#         table_name = f"t_{timeframe}_candles"
#         get_query = f"""
#         SELECT open, high, low, close, timestamp
#         FROM {table_name}
#         WHERE symbol = %s
#         ORDER BY timestamp DESC
#         LIMIT 100
#         """
#         data_frame = pd.read_sql(get_query, self.con, params=(symbol,))
#         return data_frame
