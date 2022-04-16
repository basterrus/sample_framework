from copy import deepcopy
from quopri import decodestring

import self as self

from patterns.behavioral_patterns import Subject, LogWriter


class User(Subject):
    """Класс абстрактного пользователя"""

    def __init__(self, name):
        super().__init__()
        self.name = name


class Buyer(User):
    """Класс покупателя"""

    def __init__(self, name):
        self.products = []
        super().__init__(name)


class Seller(User):
    """Класс продавца"""
    pass


class UserFactory:
    """Фабрика """
    types = {
        'buyer': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class ProductPrototype:
    """Класс прототип продукта"""

    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype, Subject):
    """Класс продукта"""

    def __init__(self, name, category):
        super().__init__()
        self.name = name
        self.category = category
        self.category.products.append(self)
        self.buyer = []

    def __getitem__(self, item):
        return self.buyer[item]

    def add_buyer(self, buyer: Buyer):
        self.buyer.append(buyer)
        buyer.products.append(self)
        self.notify()


class AbstractProduct(Product):
    """Класс абстрактного продукта"""


class ProductFactory:
    types = {
        'product': AbstractProduct
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category(Subject):
    """Класс категорий"""

    auto_id = 0

    def __init__(self, name, category):
        super().__init__()
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.products = []

    def product_count(self):
        result = len(self.products)
        if self.category:
            result += self.category.product_count()
        return result


class Engine:
    """Основной интерфейс"""

    def __init__(self):
        self.sellers = []
        self.buyers = []
        self.products = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Категория с заданным id = {id} не найдена!')

    @staticmethod
    def create_product(type_, name, category):
        return ProductFactory.create(type_, name, category)

    def get_product(self, name):
        for product_ in self.products:
            if product_.name == name:
                return product_
        return None

    def get_product_by_id(self, id):
        for product_ in self.products:
            print("product", product_.id)
            if product_.id == id:
                return product_
        raise Exception(f'Продукт с заданным id= {id} не найден!')

    def get_buyer(self, name) -> Buyer:
        for item in self.buyers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Класс Singleton"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=LogWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        print('log->', text)
        self.writer.write(text)
