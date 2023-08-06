"""
A module of window add a contact.
"""


import os
import sys
import logging

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from common.log import client_log_config
from client.client_database import ClientDatabase

logger = logging.getLogger('client')


class AddContactDialog(QDialog):
    """
    Add contact dialog window
    """

    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Choose contacts to add:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.setStyleSheet("background-color: rgb(85, 85, 127);")

        self.selector_label = QLabel('ВChoose contacts to add:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Refresh list', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_ok = QPushButton('Add', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.possible_contacts_update()
        self.btn_refresh.clicked.connect(self.update_possible_contacts)

    def possible_contacts_update(self) -> None:
        """
        Getting a list of all users and a list of contacts.
         Looking for new contacts in the difference between the two received lists
        :return: None
        """
        self.selector.clear()
        contacts_list = set(self.database.get_all_contacts())
        users_list = set(self.database.get_all_known_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self) -> None:
        """
        Updating the list of possible contacts.

        :return: None
        """
        try:
            self.transport.contacts_list_update()
        except OSError:
            pass
        else:
            logger.debug('Update complete')
            self.possible_contacts_update()


if __name__ == '__main__':
    db = ClientDatabase(db_name='test_client')
    app = QApplication([])
    window = AddContactDialog(transport=None, database=db)
    window.show()
    app.exec_()
