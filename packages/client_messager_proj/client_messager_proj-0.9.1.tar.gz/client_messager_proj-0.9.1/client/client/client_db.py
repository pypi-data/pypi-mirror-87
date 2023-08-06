import os
import sys

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
import datetime
from sqlalchemy.sql import default_comparator

sys.path.append('../../../')


class ClientStorage:
    """Класс для работы с базой данной клиента"""
    class KnownUsers:
        """Класс таблица - известные пользователи"""
        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """Класс таблица - исптория сообщений"""
        def __init__(self, from_user, to_user, message):
            self.id = None
            self.from_user = from_user
            self.to_user = to_user
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Класс таблица - контакты"""
        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        path = os.path.dirname(os.getcwd())
        filename = f'client_{name}.db3'
        self.engine = create_engine(
            f'sqlite:///{os.path.join(path, filename)}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        self.metadata = MetaData()

        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String)
                      )

        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('from_user', String),
                        Column('to_user', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )

        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )

        self.metadata.create_all(self.engine)

        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Добавление контакта"""
        if not self.session.query(
                self.Contacts).filter_by(
                name=contact).count():
            contact_ = self.Contacts(contact)
            self.session.add(contact_)
            self.session.commit()

    def contacts_clear(self):
        """Очищаем таблицу списка контактов"""
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """Удаление контакта"""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Добавление известных пользователей"""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def get_contacts(self):
        """Запрос списка контактов"""
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Список известных пользователей"""
        return [user[0]
                for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """
        Проверка пользователя на присутствие
        в списке известных пользователей
        """
        if self.session.query(
                self.KnownUsers).filter_by(
                username=user).count():
            return True
        else:
            return False

    def save_message(self, from_user, to_user, message):
        """Сохраненение сообщений"""
        message_row = self.MessageHistory(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()

    def check_contact(self, contact):
        """
        Проверка пользователя на присутствие
        в списке контактов
        """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, from_who):
        """История переписки"""
        query = self.session.query(
            self.MessageHistory).filter_by(
            from_user=from_who)
        return [(history_row.from_user,
                 history_row.to_user,
                 history_row.message,
                 history_row.date) for history_row in query.all()]


# отладка
if __name__ == '__main__':
    test_db = ClientStorage('test1')
    for i in ['test3', 'test4', 'test5']:
        test_db.add_contact(i)
    test_db.add_contact('test4')
    test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    test_db.save_message(
        'test1',
        'test2',
        f'Тестовое сообщение ---- 1. Отправлено : {datetime.datetime.now()}!')
    test_db.save_message(
        'test2',
        'test1',
        f'Тестовое сообщение ---- 2. Отправлено : {datetime.datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(test_db.get_history('test2'))
    print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
    print(test_db.get_history('test3'))
    test_db.del_contact('test4')
    print(test_db.get_contacts())
