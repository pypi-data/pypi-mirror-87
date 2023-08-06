from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
import datetime
import logging
from sqlalchemy.sql import default_comparator

server_logger = logging.getLogger('server')


class ServerStorage:
    """Основной класс базы данных сервера"""
    class Users:
        """Класс таблицы - пользователи"""
        def __init__(self, name, passwd_hash):
            self.id = None
            self.name = name
            self.last_login = datetime.datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None

    class ActiveUsers:
        """Класс таблицы - активные пользователи"""
        def __init__(self, user_id, ip_address, port, login_time):
            self.id = None
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time

    class LoginHistory:
        """Класс таблицы - история входа пользователя"""
        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class UsersContacts:
        """Класс таблицы - контакты пользователя"""
        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory:
        """Класс таблицы - история сообщений пользователя"""
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.engine = create_engine(
            f'sqlite:///{path}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})

        self.metadata = MetaData()

        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_login', DateTime),
                            Column('passwd_hash', String),
                            Column('pubkey', Text)
                            )

        active_users_table = Table('ActiveUsers', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user', ForeignKey('Users.id'), unique=True),
                                   Column('ip_address', String),
                                   Column('port', Integer),
                                   Column('login_time', DateTime)
                                   )

        login_history_table = Table('LoginHistory', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', ForeignKey('Users.id')),
                                    Column('date_time', DateTime),
                                    Column('ip', String),
                                    Column('port', String)
                                    )

        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id'))
                         )

        users_history_table = Table('History', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('Users.id')),
                                    Column('sent', Integer),
                                    Column('accepted', Integer)
                                    )

        self.metadata.create_all(self.engine)

        mapper(self.Users, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.LoginHistory, login_history_table)
        mapper(self.UsersContacts, contacts)
        mapper(self.UsersHistory, users_history_table)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def login(self, username, ip_adress, port, key):
        """Фиксируем факт входа пользователя в чат"""
        query = self.session.query(self.Users).filter_by(name=username)

        if query.count():
            user = query.first()
            user.last_login = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        add_active_user = self.ActiveUsers(
            user.id, ip_adress, port, datetime.datetime.now())
        self.session.add(add_active_user)

        add_login_history = self.LoginHistory(
            user.id, datetime.datetime.now(), ip_adress, port)
        self.session.add(add_login_history)

        self.session.commit()

    def logout(self, username):
        """Фиксируем выход пользователя из чата"""
        user = self.session.query(self.Users).filter_by(name=username).first()

        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()

        self.session.commit()

    def users_list(self):
        """Выводит список всех пользователей"""
        query = self.session.query(
            self.Users.name,
            self.Users.last_login,
        )
        return query.all()

    def active_users(self):
        """Выводит список активных пользователей"""
        query = self.session.query(
            self.Users.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.Users)
        return query.all()

    def login_history(self, username=None):
        """История входа пользователя"""
        query = self.session.query(self.Users.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.Users)
        if username:
            query = query.filter(self.Users.name == username)
        return query.all()

    def count_messages(self, sender, recipient):
        """Счетчик отправленных и принятых сообщений пользователей"""
        sender = self.session.query(
            self.Users).filter_by(
            name=sender).first().id
        recipient = self.session.query(
            self.Users).filter_by(
            name=recipient).first().id

        sender_row = self.session.query(
            self.UsersHistory).filter_by(
            user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(
            self.UsersHistory).filter_by(
            user=recipient).first()
        recipient_row.accepted += 1

        self.session.commit()

    def add_contact(self, user, contact):
        """Добавление контакта"""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(
            self.Users).filter_by(
            name=contact).first()

        if not contact or self.session.query(
                self.UsersContacts).filter_by(
                user=user.id,
                contact=contact.id).count():
            return

        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Удаляем пользователя"""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(
            self.Users).filter_by(
            name=contact).first()

        if not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete()

        self.session.commit()

    def get_contacts(self, username):
        """Возвращает список контактов пользователя"""
        user = self.session.query(self.Users).filter_by(name=username).one()

        query = self.session.query(self.UsersContacts, self.Users.name). \
            filter_by(user=user.id). \
            join(self.Users, self.UsersContacts.contact == self.Users.id)

        return [contact[1] for contact in query.all()]

    def message_history(self):
        """История сообщений"""
        query = self.session.query(
            self.Users.name,
            self.Users.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.Users)
        return query.all()

    def add_user(self, name, passwd_hash):
        '''Регистрация пользователя.Запись в БД'''
        user_row = self.Users(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        '''удаление пользователя из БД'''
        user = self.session.query(self.Users).filter_by(name=name).first()
        self.session.query(self.Users).filter_by(name=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(
            self.UsersContacts).filter_by(
            contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.Users).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        '''получения хэша пароля пользователя.'''
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        '''получения публичного ключа пользователя.'''
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        '''проверка существование пользователя в БД'''
        if self.session.query(self.Users).filter_by(name=name).count():
            return True
        else:
            return False


if __name__ == '__main__':
    test_db = ServerStorage('server_database.db3')
    test_db.add_user('user_1', '12345')
    test_db.login('user_1', '192.168.1.4', 8888, '12345')
    #test_db.login('user_2', '192.168.1.5', 7777, '12345')
    # print(test_db.active_users())
    #
    # test_db.logout('user_1')
    # print(test_db.active_users())
    #
    # test_db.login_history('user_1')
    # print(test_db.users_list())
    print(test_db.check_user('user_2'))
    # print(test_db.login_history('user_1'))
    # print(test_db.add_contact('user_1', 'user_2'))
    # print(test_db.get_contacts('user_1'))
    # print(test_db.users_list())
