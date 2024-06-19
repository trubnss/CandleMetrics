import sqlite3
import pandas as pd


class DatabaseManager:
    def __init__(self, db_connection=None):
        self.con = db_connection or sqlite3.connect("../db.sqlite")

    def create_table(self, table_name):
        cursor = self.con.cursor()
        create_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (symbol) REFERENCES cryptocurrencies (symbol)
        )
        """
        cursor.execute(create_query)
        self.con.commit()

    def create_pair(self, symbol):
        cursor = self.con.cursor()
        create_query = """
        CREATE TABLE IF NOT EXISTS crypto_pair(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE
        )
        """
        cursor.execute(create_query)
        cursor.execute(
            "INSERT OR IGNORE INTO crypto_pair (symbol) VALUES (?)", (symbol,)
        )
        self.con.commit()

    def store_candles(self, symbol, timeframe, candles):
        table_name = f"t_{timeframe}_candles"
        self.create_pair(symbol)
        self.create_table(table_name)

        cursor = self.con.cursor()
        insert_query = f"""
        INSERT INTO {table_name} (
            symbol,
            open,
            high,
            low,
            close,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """
        for candle in candles:
            cursor.execute(
                insert_query,
                (
                    symbol,
                    candle["open"],
                    candle["high"],
                    candle["low"],
                    candle["close"],
                    candle["timestamp"],
                ),
            )
        self.con.commit()

    def get_candles(self, symbol, timeframe):
        table_name = f"t_{timeframe}_candles"
        get_query = f"""
        SELECT open, high, low, close, timestamp
        FROM {table_name}
        WHERE symbol = ?
        ORDER BY timestamp DESC
        LIMIT 100
        """
        data_frame = pd.read_sql(get_query, self.con, params=(symbol,))
        return data_frame
