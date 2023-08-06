"""
A server's data base module based on SQLAlchemy declarative way.
"""

import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql import default_comparator

BASEDIR = os.getcwd()
DB_FILENAME = 'server_db.sqlite3'
DB_PATH = os.path.join(BASEDIR, DB_FILENAME)


class ServerDatabase:
    """
    A class of server database
    """

    # use declarative way
    Base = declarative_base()

    #  ------ Tables ------

    class AllUsers(Base):
        """
        All Users table
        """
        __tablename__ = 'all_users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
        password = Column(String)
        last_conn = Column(DateTime)

        def __init__(self, username, password):
            self.username = username
            self.password = password
            self.last_conn = datetime.now()

        def __repr__(self):
            return f'User: {self.username}'

    class ActiveUsers(Base):
        """
        Active users table. (Logged in)
        """
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        time_conn = Column(DateTime)

        def __init__(self, user, ip, port, time_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.time_conn = time_conn

        def __repr__(self):
            return f'{self.user} {self.ip}: {self.port}, {self.time_conn}'

    class LoginHistory(Base):
        """
        History of user's login table
        """
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'))
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __init__(self, user, ip, port, last_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_conn = last_conn

        def __repr__(self):
            return f'User last login: {self.last_conn}'

    class UsersContacts(Base):
        """
        User's contacts book table
        """
        __tablename__ = 'users_contacts'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'))
        contact = Column(String, ForeignKey('all_users.id'))

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    class UsersHistory(Base):
        """
        Users input/output messages counts table
        """
        __tablename__ = 'users_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user, sent=0, accepted=0):
            self.id = None
            self.user = user
            self.sent = sent
            self.accepted = accepted

    #  ------ Methods ------

    def __init__(self, db_path: str) -> None:
        self.engine = create_engine(
            f'sqlite:///{db_path}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        self.Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        # Clear active users table
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def _add_active_user(self, user: AllUsers, ip: str, port: str, time_conn: datetime) -> None:
        """
        Add the user in table of active users.

        :param user: An instance of AllUsers table.
        :param ip: An ip address.
        :param port: An ip port.
        :param time_conn: A time of connection.
        :return: None
        """
        new_active_user = self.ActiveUsers(
            user=user.id,
            ip=ip,
            port=port,
            time_conn=time_conn)
        self.session.add(new_active_user)
        self.session.commit()

    def _add_history(self, user: AllUsers, ip: str, port: str, last_conn: datetime) -> None:
        """
        Adding a login history record for a user.

        :param user: An instance of AllUsers table.
        :param ip: An ip address.
        :param port: An ip port.
        :param last_conn: A time of last connection.
        :return:
        """
        user_history = self.LoginHistory(user=user.id, ip=ip, port=port, last_conn=last_conn)
        self.session.add(user_history)
        self.session.commit()

    def user_login(self, username: str, ip: str, port: str) -> None:
        """
        An user login handler.

        :param username: An username of user.
        :param ip: An ip address.
        :param port: An ip port.
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(username=username).first()
        if user:
            user.last_conn = datetime.now()
            self.session.commit()

        self._add_active_user(user=user, ip=ip, port=port, time_conn=datetime.now())
        self._add_history(user=user, ip=ip, port=port, last_conn=datetime.now())

    def user_logout(self, username: str) -> None:
        """
        An user logout handler.

        :param username: An username of user.
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(username=username).first()
        if user:
            self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
            self.session.commit()

    def get_users_list(self) -> list:
        """
        Getting the list of all existing users.

        :return: A list of all existing users.
        """
        query = self.session.query(
            self.AllUsers.username,
            self.AllUsers.last_conn,
        )
        return query.all()

    def get_active_users_list(self) -> list:
        """
        Getting the list of all active users.

        :return: A list of all active users.
        """
        query = self.session.query(
            self.AllUsers.username,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(
            self.AllUsers
        )
        return query.all()

    def get_login_history(self, username: str) -> list:
        """
        Getting a history of login for a specific user.

        :param username: An username to search history.
        :return: A list of historical records.
        """
        query = self.session.query(
            self.LoginHistory,
            self.AllUsers,
        ).join(
            self.AllUsers
        ).filter_by(
            username=username
        )
        return query.all()

    def add_user_contact(self, user: str, contact: str) -> None:
        """
        Removing the contact in the user's contact table.

        :param user: n username of a user.
        :param contact: An username of a contact.
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(username=user).first()
        contact = self.session.query(self.AllUsers).filter_by(username=contact).first()

        if not user or not contact or self.session.query(
                self.UsersContacts).filter_by(
            user=user.id,
            contact=contact.id).count():
            return

        new_contact = self.UsersContacts(user.id, contact.id)
        self.session.add(new_contact)
        self.session.commit()

    def remove_user_contact(self, user: str, contact: str) -> None:
        """
        Removing the contact form the user's contact table.

        :param user: An username of a user
        :param contact: An username of a contact.
        :return: None
        """
        user = self.session.query(self.AllUsers).filter_by(username=user).first()
        contact = self.session.query(self.AllUsers).filter_by(username=contact).first()

        if not user or not contact:
            return

        self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete()
        self.session.commit()

    def get_user_contacts(self, username: str) -> list:
        """
        Getting a list of contacts for the user.

        :param username: An username of a user
        :return: A list of contacts
        """
        user = self.session.query(self.AllUsers).filter_by(username=username).one()
        query = self.session.query(
            self.UsersContacts,
            self.AllUsers.username
        ).filter_by(
            user=user.id
        ).join(
            self.AllUsers, self.UsersContacts.contact == self.AllUsers.id
        )
        return [contact[1] for contact in query.all()]

    def inc_message_counter(self, sender: str, recipient: str) -> None:
        """
        Increasing of a statistic of received / sent messages for the users.

        :param sender: Username of sender.
        :param recipient: Username of recipient.
        :return: None
        """
        sender = self.session.query(self.AllUsers).filter_by(username=sender).first()
        recipient = self.session.query(self.AllUsers).filter_by(username=recipient).first()

        sender_counter = self.session.query(self.UsersHistory).filter_by(user=sender.id).first()
        recipient_counter = self.session.query(
            self.UsersHistory).filter_by(
            user=recipient.id).first()
        if sender_counter and recipient_counter:
            sender_counter.sent += 1
            recipient_counter.accepted += 1
        else:
            new_sender_counter = self.UsersHistory(
                user=sender.id,
                sent=1,
            )
            self.session.add(new_sender_counter)

            new_recipient_counter = self.UsersHistory(
                user=recipient.id,
                accepted=1,
            )
            self.session.add(new_recipient_counter)

        self.session.commit()

    def get_message_counter(self) -> list:
        """
        Gettin of a statistic of received / sent messages for all users.

        :return: A list of statistic's records.
        """
        query = self.session.query(
            self.AllUsers.username,
            self.AllUsers.last_conn,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)

        return query.all()

    def is_exist_user(self, username: str) -> bool:
        """
        Checking if the user exists in the table AllUsers.

        :param username: An username of user for checking.
        :return: True if the user is exists, else False.
        """
        if self.session.query(self.AllUsers).filter_by(username=username).count():
            return True
        return False

    def add_user(self, username: str, password: str) -> None:
        """
        Adding new user in AllUsers table.

        :param username: An username.
        :param password: A hash of password.
        :return: None
        """
        new_user = self.AllUsers(
            username=username,
            password=password
        )
        self.session.add(new_user)
        self.session.commit()

    def remove_user(self, username: str) -> None:
        """
        Removing an existing user.

        :param username: An username of user for removing
        :return: None
        """
        self.session.query(self.AllUsers).filter_by(username=username).delete()
        self.session.commit()

    def get_passwd_hash(self, username: str) -> str:
        """
        Getting hash of password for a specific user.

        :param username: An username of user.
        :return: Hash of password.
        """
        query = self.session.query(self.AllUsers.password).filter_by(username=username).first()
        return query[0]


if __name__ == '__main__':
    db = ServerDatabase(db_path=DB_FILENAME)
    db.user_login(username='client_1', ip='192.168.1.4', port='8888')
    db.user_login(username='client_2', ip='192.168.1.5', port='7777')
    # выводим список кортежей - активных пользователей
    print("db.get_active_users_list() =", db.get_active_users_list())
    # выполянем 'отключение' пользователя
    db.user_logout('client_1')
    print("db.get_users_list() =", db.get_users_list())
    # выводим список активных пользователей
    print("db.get_active_users_list() =", db.get_active_users_list())
    # запрашиваем историю входов по пользователю
    print("db.get_login_history('client_1') =", db.get_login_history('client_1'))
    # # выводим список известных пользователей
    print("db.get_users_list() =", db.get_users_list())

    db.add_user_contact(user='client_1', contact='client_2')
    print("db.get_user_contacts(username='client_1') =", db.get_user_contacts(username='client_1'))
    db.remove_user_contact(user='client_1', contact='client_2')
    print("db.get_user_contacts(username='client_1') =", db.get_user_contacts(username='client_1'))

    db.inc_message_counter(sender='client_1', recipient='client_2')
    print("db.get_message_counter() =", db.get_message_counter())
