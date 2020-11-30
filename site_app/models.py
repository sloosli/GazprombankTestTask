from uuid import uuid4
from . import db


class User(db.Model):
    __tablename__ = 'users'
    guid = db.Column(db.String(40), primary_key=True)
    user_family = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    user_patronymic = db.Column(db.String(50))
    user_sex = db.Column(db.Integer)
    user_age = db.Column(db.Integer)
    user_living_town = db.Column(db.String(50))
    user_question = db.Column(db.String(255))

    def __init__(self, data):
        db.Model.__init__(self)
        for field in User.get_arguments():
            setattr(self, field, data[field])
        self.guid = str(uuid4())

    @staticmethod
    def get_arguments():
        # Список полей в формате:
        # название : (тип, размер)
        # для чисел размер указан исключительно для проверки
        return {
            'user_family': ('string', 50),
            'user_name': ('string', 50),
            'user_patronymic': ('string', 50),
            'user_sex': ('integer', -1),
            'user_age': ('integer', -1),
            'user_living_town': ('string', 50),
            'user_question': ('string', 255),

        }

    @staticmethod
    def validate(data):
        """
        Проверка словаря перед записью сущности пользователя в базу
        :param data: словарь, опыисывающий сущность
        :return errors: словарь ошибок, пустой, если валидация успешна
        """
        errors = set()
        for key, (_type, length) in User.get_arguments().items():
            validate = True
            # Если поле должно быть строкой то проверяем на наличие и размер
            if _type == 'string':
                value = data.get(key, '')
                validate = len(value) != 0 and len(value) <= length
            # Если число, то проверяем на тип и ненулевую величину
            # а также не превосходит ли разумных пределов
            elif _type == 'integer':
                try:
                    validate = 0 < int(data.get(key, -1)) < 2 ** 16
                except ValueError:
                    validate = False
            # Если проверка поля не прошла, добавляем его в список ошибок
            if not validate:
                errors.add(key)

        # Проверяем наличие города в словаре
        town = Dictionary.query.filter_by(
            id=data['user_living_town'],
            type_id=Dictionary.Type.town).first()
        if not town:
            errors.add('user_living_town')

        return errors


class Dictionary(db.Model):
    __tablename__ = 'dictionary'
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    value = db.Column(db.String(255))

    class Type:
        town = 1
