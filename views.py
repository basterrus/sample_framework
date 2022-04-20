from framework.patterns.unit_of_work import UnitOfWork
from framework.templator import render
from framework.patterns.behavioral_patterns import BaseSerializer, EmailNotifier, SmsNotifier, ListView, CreateView
from framework.patterns.сreational_patterns import Engine, Logger, MapperRegistry
from framework.patterns.structural_patterns import Route, Debug

engine = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
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
@Debug(name='Contacts')
class Contacts:
    """Класс страницы контакты"""

    def __call__(self, request):
        return '200 OK', render('contacts.html')


@Route(routes=routes, url='/categories/')
@Debug(name='CategoryList')
class CategoriesListView(ListView):
    queryset = engine.categories
    template_name = 'categories_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('categories')
        return mapper.all()


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
            # new_category.observers.append(email_notifier)
            # new_category.observers.append(sms_notifier)
            engine.categories.append(new_category)
            new_category.mark_new()
            UnitOfWork.get_current().commit()

            return '200 OK', render('categories_list.html', objects_list=engine.categories)
        else:
            categories = engine.categories
            return '200 OK', render('create_category.html', categories=categories)


@Route(routes=routes, url='/products/')
@Debug(name='ProductsList')
class ProductsList(ListView):
    """Класс списка товаров"""
    queryset = engine.products
    template_name = 'products_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('products')
        return mapper.all()


#
# @Route(routes=routes, url='/products/list/')
# @Debug(name='ProductsList')
# class ProductsList:
#     """Класс списка товаров"""
#
#     def __call__(self, request):
#         logger.log('Список продуктов')
#         products = engine.products
#         return '200 OK', render('products_list.html', objects_list=products)


@Route(routes=routes, url='/products/add/')
class ProductsCreate:
    """Класс создания товаров"""

    category_id = -1

    @Debug(name='CreateProduct')
    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = engine.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = engine.find_category_by_id(int(self.category_id))
                new_products = engine.create_product('product', name, category)

                # new_products.observers.append(email_notifier)
                # new_products.observers.append(sms_notifier)

                engine.products.append(new_products)

                new_products.mark_new()
                UnitOfWork.get_current().commit()

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
                return '200 OK', 'No products have been added yet'


@Route(routes, url='/products/copy/')
class ProductCopy:
    """Класс копирования продукта"""

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
            return '200 OK', 'No products have been added yet'


def not_found_404_view(request):
    return '404 WHAT', [b'404 not found!']


@Route(routes=routes, url='/api/')
class ProductApi:
    """Класс API Views"""

    @Debug(name='ProductApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(engine.products).save()


@Route(routes=routes, url='/buyers/')
class BuyersListView(ListView):
    queryset = engine.buyers
    template_name = 'buyers_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('buyers')
        return mapper.all()


@Route(routes=routes, url='/buyers/create/')
class BuyerCreateView(CreateView):
    template_name = 'create_buyers.html'

    def create_obj(self, data: dict):
        username = data['username']
        username = engine.decode_value(username)
        first_name = data['first_name']
        first_name = engine.decode_value(first_name)
        last_name = data['last_name']
        last_name = engine.decode_value(last_name)

        new_obj = engine.create_user('buyers', username, first_name, last_name)
        engine.buyers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@Route(routes=routes, url='/buyers/add/')
class CreateBuyersViews(CreateView):
    queryset = engine.buyers
    template_name = 'buyers_list_with_products.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = engine.products
        context['buyers'] = engine.buyers
        return context

    def create_obj(self, data: dict):
        product_name = data['product_name']
        product_name = engine.decode_value(product_name)
        product = engine.get_product(product_name)
        buyer_name = data['buyer_name']
        buyer_name = engine.decode_value(buyer_name)
        buyer = engine.get_buyer(buyer_name)
        product.add_buyer(buyer)
