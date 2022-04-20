from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect
from framework.exeptions import RecordNotFoundException, DbCommitException, DbUpdateException, DbDeleteException
from framework.patterns.behavioral_patterns import Subject, LogWriter
from framework.patterns.unit_of_work import DomainObject


class User(Subject):
    """Класс абстрактного пользователя"""

    def __init__(self, username, first_name, last_name):
        super().__init__()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class Buyer(User, DomainObject):
    """Класс покупателя"""

    def __init__(self, username, first_name, last_name):
        self.products = []
        super().__init__(username, first_name, last_name)


class Seller(User):
    """Класс продавца"""
    pass


class UserFactory:
    """Фабрика Users"""
    types = {
        'buyers': Buyer,
        'seller': Seller
    }

    @classmethod
    def create(cls, type_, username, first_name, last_name):
        return cls.types[type_](username, first_name, last_name)


class ProductPrototype:
    """Класс прототип продукта"""

    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype, Subject, DomainObject):
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
    pass


class ProductFactory:
    types = {
        'product': AbstractProduct
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category(Subject, DomainObject):
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
    def create_user(type_, username, first_name, last_name):
        return UserFactory.create(type_, username, first_name, last_name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        print(self.categories)
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


connection = connect('database/database.sqlite')


class ProductsMapper:
    """Класс маппер для модели Products"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'products'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            print(item)
            id, name = item
            category = Product(name)
            category.id = id
            result.append(category)
        return result


class CategoryMapper:
    """Класс маппер для модели Categories"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'categories'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, category = item
            category = Category(name, category)
            category.id = id
            result.append(category)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, category) VALUES (?, ?)"
        self.cursor.execute(statement, (obj.name, obj.category))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class BuyersMapper:
    """Класс маппер для Buyers"""

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'buyers'

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            print(item)
            id, username, first_name, last_name = item
            buyer = Buyer(username, first_name, last_name)
            buyer.id = id
            result.append(buyer)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Buyer(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (username, first_name, last_name) VALUES (?, ?, ?)"
        self.cursor.execute(statement, (obj.username, obj.first_name, obj.last_name))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'buyers': BuyersMapper,
        'categories': CategoryMapper,
        'products': ProductsMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Buyer):
            return BuyersMapper(connection)
        elif isinstance(obj, Product):
            return ProductsMapper(connection)
        elif isinstance(obj, Category):
            return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
