from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator
from modules.variables import *
import datetime


class ServerStorage:
    """
    Класс - оболочка для работы с базой данных сервера.
    В качестве базы данных выбрана - SQLite, реализован с помощью
    SQLAlchemy ORM.
    """
    class Users:
        """Класс - отображение таблицы всех пользователей."""

        def __init__(self, username, password_hash):
            self.name = username
            self.last_session = datetime.datetime.now()
            self.password_hash = password_hash
            self.pubkey = None
            self.id = None

    class ActiveUsers:
        """Класс - отображение таблицы активных пользователей."""

        def __init__(self, user_id, ip_addr, port, session_time):
            self.user = user_id
            self.ip_address = ip_addr
            self.port = port
            self.session_time = session_time
            self.id = None

    class SessionsHistory:
        """Класс - отображение таблицы истории входов."""

        def __init__(self, name, date, ip, port):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port

    class UsersContacts:
        """Класс - отображение таблицы контактов пользователей."""

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory:
        """Класс - отображение таблицы истории действий."""

        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.database_engine = create_engine(
            f'sqlite:///{path}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})
        self.metadata = MetaData()

        users_table = Table('Users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String, unique=True),
                            Column('last_session', DateTime),
                            Column('password_hash', String),
                            Column('pubkey', Text)
                            )

        active_users_table = Table(
            'Active_users', self.metadata, Column(
                'id', Integer, primary_key=True), Column(
                'user', ForeignKey('Users.id'), unique=True), Column(
                'ip_address', String), Column(
                    'port', Integer), Column(
                        'session_time', DateTime))

        user_session_history = Table('Sessions_history', self.metadata,
                                     Column('id', Integer, primary_key=True),
                                     Column('name', ForeignKey('Users.id')),
                                     Column('date_time', DateTime),
                                     Column('ip_address', String),
                                     Column('port', String)
                                     )

        contacts = Table('Contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('user', ForeignKey('Users.id')),
                         Column('contact', ForeignKey('Users.id'))
                         )

        users_history = Table('History', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user', ForeignKey('Users.id')),
                              Column('sent', Integer),
                              Column('accepted', Integer)
                              )

        self.metadata.create_all(self.database_engine)

        mapper(self.Users, users_table)
        mapper(self.ActiveUsers, active_users_table)
        mapper(self.SessionsHistory, user_session_history)
        mapper(self.UsersContacts, contacts)
        mapper(self.UsersHistory, users_history)

        session_ = sessionmaker(bind=self.database_engine)
        self.session = session_()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip_addr, port, key):
        """
        Метод выполняющийся при входе пользователя, отмечает в базу данных факт входа
        Обновляет открытый ключ пользователя при его изменении.
        """
        user_check = self.session.query(self.Users).filter_by(name=username)
        if user_check.count():
            user = user_check.first()
            user.last_session = datetime.datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        new_active_user = self.ActiveUsers(
            user.id, ip_addr, port, datetime.datetime.now())
        self.session.add(new_active_user)

        history = self.SessionsHistory(
            user.id, datetime.datetime.now(), ip_addr, port)
        self.session.add(history)

        self.session.commit()

    def user_register(self, name, password_hash):
        """
        Метод регистрации пользователя.
        Принимает имя и хэш пароля, создаёт запись в таблице статистики.
        """
        user_row = self.Users(name, password_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        """Метод удаляющий пользователя из базы."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(
            self.SessionsHistory).filter_by(
            name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(
            self.UsersContacts).filter_by(
            contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.Users).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        """Метод получения хэша пароля пользователя."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.password_hash

    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""
        user = self.session.query(self.Users).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        """Метод проверяющий существование пользователя."""
        if self.session.query(self.Users).filter_by(name=name).count():
            return True
        else:
            return False

    def user_logout(self, username):
        """Метод отмечающий отключения пользователя."""
        user = self.session.query(self.Users).filter_by(name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        """Метод возвращающий список известных пользователей со временем последнего входа."""
        query = self.session.query(
            self.Users.name,
            self.Users.last_session,
        )

        return query.all()

    def active_users_list(self):
        """Метод возвращающий список активных пользователей."""
        query = self.session.query(
            self.Users.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.session_time
        ).join(self.Users)

        return query.all()

    def session_history(self, username=None):
        """Метод возвращающий историю входов."""
        query = self.session.query(
            self.Users.name,
            self.SessionsHistory.date_time,
            self.SessionsHistory.ip_address,
            self.SessionsHistory.port
        ).join(self.Users)
        if username:
            query = query.filter(self.Users.name == username)
        return query.all()

    def marking_message(self, sender, recipient):
        """Метод записывающий в таблицу статистики факт передачи сообщения."""
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
        """Метод добавления контакта для пользователя."""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(
            self.Users).filter_by(
            name=contact).first()

        if not contact or self.session.query(
                self.UsersContacts).filter_by(
                user=user.id,
                contact=contact.id).count():
            return

        new_contact = self.UsersContacts(user.id, contact.id)
        self.session.add(new_contact)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Метод удаления контакта пользователя."""
        user = self.session.query(self.Users).filter_by(name=user).first()
        contact = self.session.query(
            self.Users).filter_by(
            name=contact).first()

        if not contact:
            return

        self.session.query(
            self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            contact.id == self.UsersContacts.contact).delete()

        self.session.commit()

    def get_contacts(self, username):
        """Метод возвращающий список контактов пользователя."""
        user = self.session.query(self.Users).filter_by(name=username).one()
        query = self.session.query(
            self.UsersContacts,
            self.Users.name).filter_by(
            user=user.id). join(
            self.Users,
            self.UsersContacts.contact == self.Users.id)

        return [contact[1] for contact in query.all()]

    def message_history(self):
        """Метод возвращающий статистику сообщений."""
        query = self.session.query(
            self.Users.name,
            self.Users.last_session,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.Users)

        return query.all()


if __name__ == '__main__':
    test = ServerStorage()
    test.user_login('1111', '192.168.1.4', 8888)
    test.user_login('2222', '192.168.1.5', 5555)
    print(test.users_list())
    # print(test.active_users_list())
    # test.user_logout('user_1')
    # print(test.active_users_list())
    # test.session_history('user_1')
    test.add_contact('1111', '2222')
    test.marking_message('1111', '2222')
    print(test.get_contacts('1111'))
    print(test.message_history())
