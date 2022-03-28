from datetime import datetime
from wsgiref.simple_server import make_server
from urls import routes, fronts
from framework import Application

application = Application(routes, fronts)

with make_server('127.0.0.1', 8000, application) as httpd:
    print(f"Сервер запущен на порту 8000 - {datetime.now()}")
    httpd.serve_forever()
