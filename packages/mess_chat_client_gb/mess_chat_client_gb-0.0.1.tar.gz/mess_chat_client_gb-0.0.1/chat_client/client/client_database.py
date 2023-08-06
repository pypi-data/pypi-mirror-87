"""
A module of client's data base. This module based on SQLAlchemy declarative way.
"""

import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql import default_comparator

BASEDIR = os.getcwd()


class ClientDatabase:
    """
    A class of clients database
    """

    # use declarative way
    Base = declarative_base()

    #  ------ Tables ------

    class KnownUsers(Base):
        """
        Known users table
        """
        __tablename__ = 'known_users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)

        def __init__(self, username):
            self.id = None
            self.username = username

        def __repr__(self):
            return f'User: {self.username}'

    class MessageHistory(Base):
        """
        User's message history table
        """
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.now()

    class Contacts(Base):
        """
        Users contacts table
        """
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)

        def __init__(self, contact):
            self.id = None
            self.username = contact

    #  ------ Methods ------

    def __init__(self, my_username: str) -> None:
        self.my_username = my_username
        db_name = my_username
        db_filename = os.path.join(BASEDIR, f"{db_name}.sqlite3")
        self.engine = create_engine(
            f'sqlite:///{db_filename}',
            echo=False,
            pool_recycle=7200,
            connect_args={'check_same_thread': False},
            poolclass=StaticPool,
        )
        self.Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        # Clear Contacts and Known Users table, to get contacts from server
        self.session.query(self.Contacts).delete()
        self.session.query(self.KnownUsers).delete()
        self.session.commit()

    def get_all_contacts(self) -> list:
        """
        Get all users from the contacts table and return a list of usernames.

        :return: List of usernames
        """
        return [contact[0] for contact in self.session.query(self.Contacts.username).all()]

    def add_contact(self, contact: str) -> None:
        """
        Add a new user to the contact table if he was not there yet.

        :param contact: A new contact username
        :return: None
        """
        if not self.session.query(self.Contacts).filter_by(username=contact).count():
            new_contact = self.Contacts(contact=contact)
            self.session.add(new_contact)
            self.session.commit()

    def is_contact(self, contact: str) -> bool:
        """
        Checking the presence of a user in the contact tables.

        :param contact: A contact username
        :return: True if a user in the contact table, else False
        """
        if self.session.query(self.Contacts).filter_by(username=contact).count():
            return True
        return False

    def del_contact(self, contact: str) -> None:
        """
        Removing a user from the contact table.

        :param contact: A contact username
        :return: None
        """
        self.session.query(self.Contacts).filter_by(username=contact).delete()

    def get_all_known_users(self) -> list:
        """
        Get all users from the known_users table and return a list of usernames.

        :return: List of usernames
        """
        return [user[0] for user in self.session.query(self.KnownUsers.username).all()]

    def add_known_users(self, users_list: list) -> None:
        """
        Add each user from the list to the table of known users.

        :param users_list: List of usernames to add
        :return: None
        """
        for user in users_list:
            user_row = self.KnownUsers(username=user)
            self.session.add(user_row)
        self.session.commit()

    def is_known_user(self, username: str) -> bool:
        """
        Checking the presence of a user in the known_users tables.

        :param username: A username
        :return: True if a user in the known_users table, else False
        """
        if self.session.query(self.KnownUsers).filter_by(username=username).count():
            return True
        return False

    def save_message_history(self, contact: str, direction: str, message: str) -> None:
        """
        Save message for message's history

        :param contact: А username of massage far end recipient / sender.
        :param direction: 'in or 'out'
        :param message:
        :return: None
        """
        message_row = self.MessageHistory(contact=contact, direction=direction, message=message)
        self.session.add(message_row)
        self.session.commit()

    def get_message_history(self, contact=None) -> list:
        """
        Get a list of messages from message history.

        :param contact: А username of massage far end recipient / sender.
        :return: A list of massages from message's history
        """
        query = self.session.query(self.MessageHistory)
        if contact:
            query = query.filter_by(contact=contact)
        return [
            (history_row.contact, history_row.direction, history_row.message, history_row.date)
            for history_row in query.all()
        ]


if __name__ == '__main__':

    db = ClientDatabase(my_username='test_client')

    for i in ['test_1', 'test_2', 'test_3']:
        db.add_contact(contact=i)
    db.add_contact(contact='test_2')
    print("db.is_contact(contact='test_3') =", db.is_contact(contact='test_3'))
    db.del_contact(contact='test_3')
    print("db.is_contact(contact='test_3') =", db.is_contact(contact='test_3'))
    print("db.get_all_contacts() =", db.get_all_contacts())

    db.add_known_users(['test_1', 'test_2', 'test_3', 'test_4', 'test_5'])
    print("db.is_known_user(username='test_2') =", db.is_known_user(username='test_2'))
    print("db.get_all_known_users() =", db.get_all_known_users())

    db.save_message_history(contact='test_2', direction='out',
                            message=f'Tестовое сообщение test_1 -> test_2 от {datetime.now()}!')
    db.save_message_history(contact='test_2', direction='in',
                            message=f'Tестовое сообщение test_2 -> test_1 от {datetime.now()}!')
    print("db.get_message_history() =", db.get_message_history())
    print("db.get_message_history(contact='test_2') =", db.get_message_history(contact='test_2'))
