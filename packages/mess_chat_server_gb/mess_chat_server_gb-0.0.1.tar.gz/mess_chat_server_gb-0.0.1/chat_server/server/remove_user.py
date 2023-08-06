"""
A module of remove a user window
"""


import os
import sys

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QApplication
from PyQt5.QtCore import Qt

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from server.server_core import ChatServerCore
from server.server_database import ServerDatabase


class RemoveUser(QDialog):
    """
    Remove existing user class
    """

    def __init__(self, database, server):
        super().__init__()
        self.database = database
        self.server = server

        self.setFixedSize(350, 120)
        self.setWindowTitle('Removing user')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Select the user to delete:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_ok = QPushButton('Remove', self)
        self.btn_ok.setFixedSize(100, 30)
        self.btn_ok.move(230, 20)
        self.btn_ok.clicked.connect(self.remove_user)

        self.btn_cancel = QPushButton('Cancel', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.all_users_fill()

    def all_users_fill(self) -> None:
        """
        Gets registred users from the database and make user's list.

        :return: None
        """
        self.selector.addItems(
            [item[0] for item in self.database.get_users_list()]
        )

    def remove_user(self) -> None:
        """
        Removing the user from the database.

        :return: None
        """
        self.database.remove_user(username=self.selector.currentText())
        self.server.user_disconnect(username=self.selector.currentText())
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    db = ServerDatabase('server_db_test.sqlite3')
    server_core = ChatServerCore(
        address='0.0.0.0',
        port=7777,
        database=db
    )
    dial = RemoveUser(database=db, server=server_core)
    dial.show()
    app.exec_()
