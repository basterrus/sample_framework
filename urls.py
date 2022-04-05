from datetime import date
import views


routes = {
    '/': views.index_view,
    '/about/': views.about_view,
    '/contacts/': views.contact_view
}


def secret_front(request):
    request['todata'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
