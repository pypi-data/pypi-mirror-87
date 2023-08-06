"""
A module of window deleting a contact.
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


class DelContactDialog(QDialog):
    """
    Deleting contact dialog window
    """

    def __init__(self, database) -> None:
        super().__init__()
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Choose contacts to delete:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)
        self.setStyleSheet("background-color: rgb(85, 85, 127);")

        self.selector_label = QLabel('Choose contacts to delete:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Delete', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        # Contact placeholder to remove
        self.selector.addItems(sorted(self.database.get_all_contacts()))


if __name__ == '__main__':
    db = ClientDatabase(db_name='test_client')
    app = QApplication([])
    window = DelContactDialog(database=db)
    window.show()
    app.exec_()
