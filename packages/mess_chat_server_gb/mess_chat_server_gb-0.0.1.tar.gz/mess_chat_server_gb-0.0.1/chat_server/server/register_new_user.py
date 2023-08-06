"""
A module of register new user window
"""

import os
import sys

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import hashlib
import binascii

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from server.server_database import ServerDatabase
from server.server_core import ChatServerCore


class RegisterNewUser(QDialog):
    """
    Register new user dialog class
    """

    def __init__(self, database, server) -> None:
        super().__init__()

        self.database = database
        self.server = server

        self.setWindowTitle('Register new user')
        self.setFixedSize(175, 183)
        self.setModal(True)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.label_username = QLabel('New user name:', self)
        self.label_username.move(10, 10)
        self.label_username.setFixedSize(150, 15)

        self.client_username = QLineEdit(self)
        self.client_username.setFixedSize(154, 20)
        self.client_username.move(10, 30)

        self.label_passwd = QLabel('Users password:', self)
        self.label_passwd.move(10, 55)
        self.label_passwd.setFixedSize(150, 15)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 75)
        self.client_passwd.setEchoMode(QLineEdit.Password)

        self.label_confirm = QLabel('Confirm password:', self)
        self.label_confirm.move(10, 100)
        self.label_confirm.setFixedSize(150, 15)

        self.client_passwd_confirm = QLineEdit(self)
        self.client_passwd_confirm.setFixedSize(154, 20)
        self.client_passwd_confirm.move(10, 120)
        self.client_passwd_confirm.setEchoMode(QLineEdit.Password)

        self.btn_ok = QPushButton('Save', self)
        self.btn_ok.move(10, 150)
        self.btn_ok.clicked.connect(self.save_data)

        self.btn_cancel = QPushButton('Exit', self)
        self.btn_cancel.move(90, 150)
        self.btn_cancel.clicked.connect(self.close)

        self.messages = QMessageBox()

        self.show()

    def save_data(self) -> None:
        """
        Save new registered user to the database.

        :return: None
        """

        if not self.client_username.text():
            self.messages.critical(
                self, 'Error!', 'Username is empty.')
            return

        if self.client_passwd.text() != self.client_passwd_confirm.text():
            self.messages.critical(
                self, 'Error', 'Passwords do not match.')
            return

        if self.database.is_exist_user(self.client_username.text()):
            self.messages.critical(
                self, 'Error', 'Пользователь уже существует.')
            return

        password_hash = self._make_hash()
        self.database.add_user(
            username=self.client_username.text(),
            password=password_hash
        )
        self.messages.information(self, 'Success', 'User registered successfully.')
        self.close()

    def _make_hash(self) -> bytes:
        """
        Make a hash of password for new register user.

        :return: A password hash
        """
        passwd_bytes = self.client_passwd.text().encode('utf-8')
        salt = self.client_username.text().lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        return binascii.hexlify(passwd_hash)


if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    db = ServerDatabase('server_db_test.sqlite3')
    server_core = ChatServerCore
    dial = RegisterNewUser(database=db, server=server_core)
    app.exec_()
