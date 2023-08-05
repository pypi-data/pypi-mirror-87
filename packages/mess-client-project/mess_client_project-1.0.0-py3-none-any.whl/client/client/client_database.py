import os
import sys
import datetime

from sqlalchemy import create_engine, Table, Column, Integer, String, Text, MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator
from modules.variables import *

sys.path.append('../')


class ClientDatabase:
    """
    Класс - оболочка для работы с базой данных клиента.
    В качестве базы данных выбрана - SQLite, реализован с помощью
    SQLAlchemy ORM.
    """
    class KnownUsers:
        """
        Класс - таблица всех пользователей.
        """

        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageHistory:
        """
        Класс - таблица статистики переданных сообщений.
        """

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """
        Класс - таблица контактов.
        """

        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        path = os.getcwd()
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(
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
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime)
                        )
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True)
                         )
        self.metadata.create_all(self.database_engine)

        mapper(self.KnownUsers, users)
        mapper(self.MessageHistory, history)
        mapper(self.Contacts, contacts)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Метод добавления контакта в базу данных"""
        if not self.session.query(
                self.Contacts).filter_by(
                name=contact).count():
            new_contact = self.Contacts(contact)
            self.session.add(new_contact)
            self.session.commit()

    def del_contact(self, contact):
        """Метод удаляющий контакта из базы данных"""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Метод заполняющий таблицу известных пользователей."""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            new_user = self.KnownUsers(user)
            self.session.add(new_user)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """Метод для сохранения сообщений в базу данных"""
        new_message = self.MessageHistory(contact, direction, message)
        self.session.add(new_message)
        self.session.commit()

    def get_contacts(self):
        """Метод для возвращения списка всех контактов"""
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Метод для возвращения списка всех известных пользователей"""
        return [user[0]
                for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """Метод для проверки существующего пользователя"""
        if self.session.query(
                self.KnownUsers).filter_by(
                username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """Метод для проверки существующего контакта"""
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, contact):
        """Метод возвращающий историю сообщений с определенным ползователем"""
        query = self.session.query(
            self.MessageHistory).filter_by(
            contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]


if __name__ == '__main__':
    test = ClientDatabase('test_user_1')
    for i in ['test_user_3', 'test_user_4', 'test_user_5']:
        test.add_contact(i)
    test.add_contact('test_user_4')
    test.add_users(['test_user_1', 'test_user_2',
                    'test_user_3', 'test_user_4', 'test_user_5'])
    test.save_message(
        'test_user_1',
        'test_user_2',
        f'тестовое сообщение от {datetime.datetime.now()}!')
    test.save_message(
        'test_user_2',
        'test_user_1',
        f'тестовое сообщение от {datetime.datetime.now()}!')
    print(test.get_contacts())
    print(test.get_users())
    print(test.check_user('test_user_1'))
    print(test.check_user('test_user_10'))
    print(test.get_history('test_user_2'))
    print(test.get_history('test_user_3'))
    test.del_contact('test_user_4')
    print(test.get_contacts())
