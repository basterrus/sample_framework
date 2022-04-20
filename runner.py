from datetime import datetime
from wsgiref.simple_server import make_server

from framework.patterns.сreational_patterns import Logger
from urls import fronts
from framework import Application
from views import routes

logger = Logger('runner')
application = Application(routes, fronts)

with make_server('127.0.0.1', 8000, application) as httpd:
    logger.log(f'Сервер запущен на порту 8000 - {datetime.now().strftime("%b %d %Y %H:%M:%S")}')
    httpd.serve_forever()
