import unittest
import sqlite3


from db_handler.db_handler import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.con = sqlite3.connect(":memory:")
        self.db_manager = DatabaseManager(self.con)
        self._create_test_tables()

    def tearDown(self):
        self.con.close()

    def _create_test_tables(self):
        cursor = self.con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crypto_pair (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE NOT NULL
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS t_1h_candles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (symbol) REFERENCES crypto_pair (symbol)
            );
            """
        )
        self.con.commit()

    def test_create_table(self):
        table_name = "test_candles"
        self.db_manager.create_table(table_name)

        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        )
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_pair(self):
        symbol = "BTCUSDT"
        self.db_manager.create_pair(symbol)

        cursor = self.con.cursor()
        cursor.execute("SELECT symbol FROM crypto_pair WHERE symbol=?;", (symbol,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], symbol)

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
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE symbol=?;", (symbol,))
        results = cursor.fetchall()
        self.assertEqual(len(results), len(candles))

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
        self.assertEqual(result_df.iloc[0]["open"], candles[1]["open"])
        self.assertEqual(result_df.iloc[1]["open"], candles[0]["open"])


if __name__ == "__main__":
    unittest.main()
