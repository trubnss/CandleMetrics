import sqlite3


def create_table(conn, table_name):
    cursor = conn.cursor()
    # Нужны уточнения по типам данных в полях таблицы!
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        timestamp TEXT NOT NULL,
        value TEXT NOT NULL,
        symbol TEXT NOT NULL,
        FOREIGN KEY (symbol) REFERENCES cryptocurrencies (symbol)
    )
    ''')


def create_database():
    conn = sqlite3.connect('crypt_candles.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cryptocurrencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL UNIQUE
    )
    ''')

    create_table(conn, 'h1')
    create_table(conn, 'd1')

    conn.commit()
    conn.close()


create_database()
