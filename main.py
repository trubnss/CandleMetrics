from wsgiref import simple_server
from api import api


if __name__ == "__main__":
    httpd = simple_server.make_server("127.0.0.1", 8000, api.app)
    httpd.serve_forever()
