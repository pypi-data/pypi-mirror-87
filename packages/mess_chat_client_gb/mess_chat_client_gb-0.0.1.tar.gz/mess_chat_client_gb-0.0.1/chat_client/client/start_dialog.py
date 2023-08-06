"""
A module of window of start dialog.
"""

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp


class UserNameDialog(QDialog):
    """
    Start dialog.
    The username and password entry window.
    """

    def __init__(self) -> None:
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Welcome!')
        self.setFixedSize(200, 200)

        self.label = QLabel('Enter username:', self)
        self.label.move(10, 5)
        self.label.setFixedSize(190, 20)

        self.client_username = QLineEdit(self)
        self.client_username.move(10, 30)
        self.client_username.setFixedSize(180, 30)

        self.label = QLabel('Enter password:', self)
        self.label.move(10, 70)
        self.label.setFixedSize(190, 20)

        self.client_password = QLineEdit(self)
        self.client_password.setEchoMode(QLineEdit.Password)
        self.client_password.move(10, 90)
        self.client_password.setFixedSize(180, 30)

        self.btn_ok = QPushButton('Start', self)
        self.btn_ok.move(10, 140)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Exit', self)
        self.btn_cancel.move(110, 140)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    def click(self) -> None:
        """
        An OK button handler.
         If username and password are entered, exiting from the dialog window.
        :return: None
        """
        if self.client_username.text() and self.client_password.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
