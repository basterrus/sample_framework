from framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import Route, Debug

engine = Engine()
logger = Logger('main')
routes = {}


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@Route(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        categories = engine.categories
        products = engine.products

        context = {
            "categories": categories,
            "products": products
        }
        return '200 OK', render('index.html', context=context)


@Route(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@Route(routes=routes, url='/contacts/')
class Contacts:
    """Класс страницы контакты"""

    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html')


@Route(routes=routes, url='/categories/')
class CategoriesList:
    """Класс списка категорий"""

    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories_list.html', objects_list=engine.categories)


@Route(routes=routes, url='/categories/add/')
class CreateCategory:
    """Класс создания категорий"""

    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = engine.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = engine.find_category_by_id(int(category_id))

            new_category = engine.create_category(name, category)

            engine.categories.append(new_category)

            return '200 OK', render('categories_list.html', objects_list=engine.categories)
        else:
            categories = engine.categories
            return '200 OK', render('create_category.html', categories=categories)


@Route(routes=routes, url='/products/')
class ProductsList:
    """Класс списка товаров"""

    @Debug(name='ProductsList')
    def __call__(self, request):
        logger.log('Список курсов')

        try:
            category = engine.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('products_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@Route(routes=routes, url='/products/add/')
class CreateProducts:
    """Класс создания товаров"""

    category_id = -1

    @Debug(name='CreateProduct')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = engine.decode_value(name)

            category = None
            if self.category_id != -1:
                category = engine.find_category_by_id(int(self.category_id))
                new_products = engine.create_product('product', name, category)
                engine.products.append(new_products)

            return '200 OK', render('products_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = engine.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_product.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@Route(routes, url='/products/copy/')
class CopyProduct:
    """Copy"""

    @Debug(name='CopyProduct')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            name = engine.decode_value(name)

            old_product = engine.get_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                engine.products.append(new_product)

            return '200 OK', render('products_list.html',
                                    objects_list=engine.products,
                                    name=new_product.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 not found!']
