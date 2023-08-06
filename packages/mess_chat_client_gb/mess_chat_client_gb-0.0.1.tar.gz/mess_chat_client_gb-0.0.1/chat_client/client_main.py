"""
A module to run a client application.
"""

import logging
import sys
from PyQt5.QtWidgets import QApplication

from client.client_database import ClientDatabase
from client.client_transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

from common.log import client_log_config
from common.cpypt import ChatCrypting

logger = logging.getLogger('client')


def get_sys_args():
    """
    Getting arguments if exists.

    :return: None
    """
    address, port, username = None, None, None
    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]

        if '-p' in sys.argv:
            _port = int(sys.argv[sys.argv.index('-p') + 1])
            if _port and 1024 < _port < 65535:
                port = _port
            else:
                logger.critical(
                    f'The port number must be int, between 1024 and 65535. Your port: "{_port}"'
                )
                raise ValueError('The port number must be int, between 1024 and 65535')

        return address, port

    except IndexError:
        logger.critical(f'The arguments must be set. Exiting. Args: "{sys.argv}"')
        sys.exit(1)


def main() -> None:
    """
    The function gets the configuration from command line arguments or configuration files.
     Initializes all application components and passes the resulting configuration to them.
    :return: None
    """
    # Загружаем параметы коммандной строки
    address, port = get_sys_args()

    # Создаём клиентокое приложение
    client_app = QApplication(sys.argv)

    # Always ask username and password
    start_dialog = UserNameDialog()
    client_app.exec_()
    if start_dialog.ok_pressed:
        username = start_dialog.client_username.text()
        password = start_dialog.client_password.text()
        del start_dialog
    else:
        sys.exit(0)

    # Записываем логи
    logger.info(f'Client started. Parameters: {address}:{port}, username - {username}')

    # Создаём объект базы данных
    database = ClientDatabase(username)

    # Создаём объект - транспорт и запускаем транспортный поток
    try:
        transport = ClientTransport(
            address=address,
            port=port,
            username=username,
            password=password,
            database=database,
            crypt=ChatCrypting
        )
    except Exception as error:
        print(error)
        sys.exit(1)
    transport.setDaemon(True)
    transport.start()

    # Создаём GUI
    main_window = ClientMainWindow(username=username, database=database, transport=transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Chat client alpha release - {username}')
    client_app.exec_()

    # Раз графическая оболочка закрылась, закрываем транспорт
    transport.transport_shutdown()
    transport.join()


if __name__ == '__main__':

    main()