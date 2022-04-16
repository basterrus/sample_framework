import quopri
from framework.requests import Get, Post


class HelloFromFake201:
    def __call__(self, request):
        logger.log("Fake answer")
        return '200 OK', 'Hello from Fake'


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Application:

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.routes_lst = urlpatterns
        self.fronts_lst = front_controllers

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = Post().get_request_params(environ)
            request['data'] = data
            print(f'POST-запрос: {Application.decode_value(data)}')

        if method == 'GET':
            request_params = Get().get_request_params(environ)
            request['request_params'] = request_params
            print(f'GET-запрос: {request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        for front in self.fronts_lst:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
