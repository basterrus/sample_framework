from copy import deepcopy
from quopri import decodestring


class User:
    """Класс абстрактного пользователя"""
    pass


class Buyer(User):
    """Класс покупателя"""
    pass


class Seller(User):
    """Класс продавца"""
    pass


class ProductPrototype:
    """Класс прототип продукта"""

    def clone(self):
        return deepcopy(self)


class ProductType(ProductPrototype):
    """Класс продукта"""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class Product:
    """Класс абстрактного продукта"""
    pass


class ProductFactory:
    types = {
        'product': Product,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class UserFactory:
    types = {
        'buyer': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category:
    """Класс категорий"""

    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """Основной интерфейс"""

    def __init__(self):
        self.sellers = []
        self.buyers = []
        self.categories = []
        self.products = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

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
        for product in self.products:
            if product.name == name:
                return product
        return None

    def get_product_by_id(self, id):
        for product in self.products:
            print("product", product.id)
            if product.id == id:
                return product
        raise Exception(f'Продукт с заданным id= {id} не найден!')

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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
