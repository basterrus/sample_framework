from framework.templates import render


def index_view(request):
    data = {'name_company': 'ООО Рога и Копыта',
            'products': ['Компьютеры', 'Серверы и СХД', 'Комплектующие', 'Программное обеспечение']}
    return '200 OK', render('index.html', **data)


def about_view(request):
    data = {'name_company': 'Наименование: ООО Рога и Копыта',
            'address': 'Адрес: Москва, ул. Б.Якиманка 123',
            'phone': 'Номер телефона: 8-800-555-3535',
            'time': 'Время работы: Пн-Пт: с 8-00 до 20-00, Сб: с 9-00 до 18-00б Вс: Выходной'}
    return '200 OK', render('about.html', **data)


def contact_view(request):
    if request.get('method') == 'POST':

        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']

        print(f'Пришло сообщение от {email} тема: {title} текст: {text}')

        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 not found!']
