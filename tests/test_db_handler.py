import unittest
import psycopg2
from db_handler.db_handler import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.con = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.db_manager = DatabaseManager(self.con)
        self._create_test_tables()

    def tearDown(self):
        cursor = self.con.cursor()
        cursor.execute("DROP TABLE IF EXISTS crypto_pair CASCADE; DROP TABLE IF EXISTS t_1h_candles CASCADE;")
        self.con.commit()
        self.con.close()

    def _create_test_tables(self):
        cursor = self.con.cursor()
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
        self.con.commit()

    def test_create_table(self):
        table_name = "test_candles"
        self.db_manager.create_table(table_name)

        cursor = self.con.cursor()
        cursor.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='{table_name}';"
        )
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], table_name)

    def test_create_pair(self):
        symbol = "BTCUSDT"
        self.db_manager.create_pair(symbol)

        cursor = self.con.cursor()
        cursor.execute("SELECT symbol FROM crypto_pair WHERE symbol=%s;", (symbol,))
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
        cursor.execute(f"SELECT * FROM {table_name} WHERE symbol=%s;", (symbol,))
        results = cursor.fetchall()
        self.assertEqual(len(results) - len(candles), 0)

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
