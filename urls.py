from datetime import date


def secret_front(request):
    request['todata'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
