"""
A module of the chat client main window.
"""

import os
import sys
import logging

from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from common.log import client_log_config
from client.del_contact import DelContactDialog
from client.add_contact import AddContactDialog
from client.client_gui import Ui_MainClientWindow


class ClientMainWindow(QMainWindow):
    """
    A chat client main window.
    """

    def __init__(self, username, database, transport) -> None:
        super().__init__()

        self._logger = logging.getLogger('client')

        # основные переменные
        self.database = database
        self.transport = transport
        self.username = username

        # Загружаем конфигурацию окна из дизайнера
        self.gui = Ui_MainClientWindow()
        self.gui.setupUi(self)

        # Кнопка "Выход"
        self.gui.menu_exit.triggered.connect(qApp.exit)

        # Кнопка отправить сообщение
        self.gui.btn_send.clicked.connect(self.send_message)

        # "добавить контакт"
        self.gui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.gui.menu_add_contact.triggered.connect(self.add_contact_window)

        # Удалить контакт
        self.gui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.gui.menu_del_contact.triggered.connect(self.delete_contact_window)

        # Дополнительные требующиеся атрибуты
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.gui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gui.list_messages.setWordWrap(True)

        # Даблклик по листу контактов отправляется в обработчик
        self.gui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self) -> None:
        """
        Disable input of the field.

        :return: None
        """
        # Надпись  - получатель.
        self.gui.label_new_message.setText('Choose recipient by double click')
        self.gui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        # Поле ввода и кнопка отправки неактивны до выбора получателя.
        self.gui.btn_clear.setDisabled(True)
        self.gui.btn_send.setDisabled(True)
        self.gui.text_message.setDisabled(True)

    def history_list_update(self) -> None:
        """
        Update the message's history list.

        :return: None
        """
        # Получаем историю сортированную по дате
        list = sorted(
            self.database.get_message_history(contact=self.current_chat),
            key=lambda item: item[3]
        )
        # Если модель не создана, создадим.
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.gui.list_messages.setModel(self.history_model)
        # Очистим от старых записей
        self.history_model.clear()
        # Берём не более 20 последних записей.
        length = len(list)
        start_index = 0
        if length > 20:
            start_index = length - 20
        # Заполнение модели записями,
        # так-же стоит разделить входящие и исходящие выравниванием и разным фоном.
        # Записи в обратном порядке, поэтому выбираем их с конца и не более 20
        for i in range(start_index, length):
            item = list[i]
            if item[1] == 'in':
                mess = QStandardItem(f'Incoming from {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(f'Outgoing to {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.gui.list_messages.scrollToBottom()

    def select_active_user(self) -> None:
        """
        Selecting the active far end user by double click by a contact.

        :return: None
        """
        # Выбранный пользователем (даблклик) находится в выделеном элементе в QListView
        self.current_chat = self.gui.list_contacts.currentIndex().data()
        # вызываем основную функцию
        self.set_active_user()

    def set_active_user(self) -> None:
        """
        Set the contact as active.

        :return: None
        """
        # Ставим надпись и активируем кнопк
        self.gui.label_new_message.setText(f'Мessage for {self.current_chat}:')
        self.gui.btn_clear.setDisabled(False)
        self.gui.btn_send.setDisabled(False)
        self.gui.text_message.setDisabled(False)

        # Заполняем окно историю сообщений по требуемому пользователю.
        self.history_list_update()

    def clients_list_update(self) -> None:
        """
        Update the contacts list.

        :return: None
        """
        contacts_list = self.database.get_all_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.gui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self) -> None:
        """
        Make a window to add a contact.

        :return: None
        """
        global select_dialog
        select_dialog = AddContactDialog(transport=self.transport, database=self.database)
        select_dialog.btn_ok.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item) -> None:
        """
        Add contact action handler.

        :param item: The contact's item from GUI
        :return: None
        """
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact: str) -> None:
        """
        Add contact to database.

        :param new_contact: The new contact username.
        :return: None
        """
        try:
            self.transport.add_contact(contact=new_contact)

        except Exception as err:
            self.messages.critical(self, 'Server error', err.text)

        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', 'Connection lost!')
                self.close()
            self.messages.critical(self, 'Error', 'Connection timeout!')

        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            self._logger.info(f'Contact added successfully {new_contact}')
            self.messages.information(self, 'Success', 'Contact added successfully.')

    def delete_contact_window(self) -> None:
        """
        Make a window to delete a contact.

        :return: None
        """
        global remove_dialog
        remove_dialog = DelContactDialog(database=self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item) -> None:
        """
        Delete contact handler.

        :param item: The contact's item from GUI.
        :return: None
        """
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except Exception as err:
            self.messages.critical(self, 'Server error', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', 'Connection lost!')
                self.close()
            self.messages.critical(self, 'Error', 'Connection timeout!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            self._logger.info(f'Contact deleted successfully {selected}')
            self.messages.information(self, 'Success', 'Contact deleted successfully.')
            item.close()
            # Если удалён активный пользователь, то деактивируем поля ввода.
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self) -> None:
        """
        Sending a message to a remote contact.

        :return: None
        """
        # Текст в поле, проверяем что поле не пустое затем забирается сообщение и поле очищается
        message_text = self.gui.text_message.toPlainText()
        self.gui.text_message.clear()
        if not message_text:
            return
        try:
            self.transport.send_message(self.current_chat, message_text)
            pass
        except Exception as err:
            self.messages.critical(self, 'Error', err)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Error', 'Connection lost!')
                self.close()
            self.messages.critical(self, 'Error', 'Connection timeout!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Error', 'Connection lost!')
            self.close()
        else:
            self.database.save_message_history(
                contact=self.current_chat, direction='out', message=message_text)
            self._logger.debug(f'Message sent for {self.current_chat}: {message_text}')
            self.history_list_update()

    @pyqtSlot(str)
    def message(self, sender) -> None:
        """
        Slot for receiving new messages.

        :param sender: The sender user.
        :return: None
        """
        if sender == self.current_chat:
            self.history_list_update()
        else:
            # Проверим есть ли такой пользователь у нас в контактах:
            if self.database.is_contact(sender):
                # Если есть, спрашиваем и желании открыть с ним чат и открываем при желании
                if self.messages.question(
                        self,
                        'A new message',
                        f'Received a new message from {sender}, open a chat?',
                        QMessageBox.Yes,
                        QMessageBox.No
                ) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                # Раз нету,спрашиваем хотим ли добавить юзера в контакты.
                if self.messages.question(
                        self,
                        'A new message',
                        f'Received a new message from {sender}.\n Add this user to contact?',
                        QMessageBox.Yes,
                        QMessageBox.No
                ) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self) -> None:
        """
        Slot lost connection.
         Gives an error message and exits the application.
        :return: None
        """
        self.messages.warning(self, 'Error', 'Connection lost!')
        self.close()

    def make_connection(self, trans_obj) -> None:
        """
        Action and slot mappings.

        :param trans_obj:
        :return: None
        """
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)
