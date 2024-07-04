import unittest
from unittest.mock import MagicMock, call

from dotenv import load_dotenv
from adapters.database_manager import DatabaseManager

load_dotenv()


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        # Мокирование psycopg2.connect
        self.mock_db_connection = MagicMock()
        self.db_manager = DatabaseManager(db_connection=self.mock_db_connection)
        self._create_test_tables()

    def _create_test_tables(self):
        mock_cursor = self.mock_db_connection.cursor.return_value
        mock_cursor.execute = MagicMock()

        # Создание таблиц
        cursor = self.mock_db_connection.cursor.return_value
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crypto_pair (
                id SERIAL PRIMARY KEY,
                symbol TEXT UNIQUE NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS t_1h_candles (
                id SERIAL PRIMARY KEY,
                symbol TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                timestamp BIGINT NOT NULL,
                FOREIGN KEY (symbol) REFERENCES crypto_pair (symbol)
            );
            """
        )
        self.mock_db_connection.commit.return_value = None

    def test_create_table(self):
        table_name = "test_candles"
        self.db_manager.create_table(table_name)

        cursor = self.mock_db_connection.cursor.return_value


        calls = [call(f"CREATE TABLE IF NOT EXISTS {table_name} ("
                      "id SERIAL PRIMARY KEY,"
                      "symbol TEXT NOT NULL,"
                      "open REAL NOT NULL,"
                      "high REAL NOT NULL,"
                      "low REAL NOT NULL,"
                      "close REAL NOT NULL,"
                      "timestamp BIGINT NOT NULL,"
                      "FOREIGN KEY (symbol) REFERENCES crypto_pair (symbol)"
                      ");")]
        cursor.execute.assert_any_call(*calls)

    def test_create_pair(self):
        symbol = "BTCUSDT"
        self.db_manager.create_pair(symbol)

        cursor = self.mock_db_connection.cursor.return_value
        calls = [call(
            "INSERT INTO crypto_pair (symbol) VALUES (%s) ON CONFLICT DO NOTHING",
            (symbol,)
        )]
        cursor.execute.assert_any_call(*calls)

    def test_store_candles(self):
        symbol = "BTCUSDT"
        timeframe = "1h"
        candles = [
            {
                "timestamp": 1620000000,
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
            },
            {
                "timestamp": 1620003600,
                "open": 105,
                "high": 115,
                "low": 95,
                "close": 110,
            },
        ]

        self.db_manager.store_candles(symbol, timeframe, candles)

        table_name = f"t_{timeframe}_candles"
        cursor = self.mock_db_connection.cursor.return_value
        calls = [call(
            f"INSERT INTO {table_name} (symbol, open, high, low, close, timestamp) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (symbol, 100, 110, 90, 105, 1620000000)
        )]
        cursor.execute.assert_any_call(*calls)

    def test_get_candles(self):
        symbol = "BTCUSDT"
        timeframe = "1h"
        candles = [
            {
                "timestamp": 1620000000,
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
            },
            {
                "timestamp": 1620003600,
                "open": 105,
                "high": 115,
                "low": 95,
                "close": 110,
            },
        ]

        self.db_manager.store_candles(symbol, timeframe, candles)
        result_df = self.db_manager.get_candles(symbol, timeframe)

        self.assertEqual(len(result_df), len(candles))


if __name__ == "__main__":
    unittest.main()
