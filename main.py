from wsgiref import simple_server

from adapters.binance_adapter import BinanceAPIHandler
from adapters.database_manager import DatabaseManager
from api.api import create_app

if __name__ == "__main__":
    binance_api_handler = BinanceAPIHandler()
    database_manager = DatabaseManager()
    app = create_app(binance_api_handler, database_manager)

    httpd = simple_server.make_server("127.0.0.1", 8000, app)
    httpd.serve_forever()
