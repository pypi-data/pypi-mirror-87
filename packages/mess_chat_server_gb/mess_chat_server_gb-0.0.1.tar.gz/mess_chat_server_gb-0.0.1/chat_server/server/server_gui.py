"""
A module with GIU elements for the server
"""

import os
import sys

from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt

BASEDIR = os.getcwd()
sys.path.append(BASEDIR)

from server.server_database import ServerDatabase


class MainWindow(QMainWindow):
    """
    The main server window class
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Exit button
        exitAction = QAction(QIcon(f'{BASEDIR}/server/exit.jpeg'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        # Refresh contact list
        self.refresh_contacts_button = QAction(QIcon(f'{BASEDIR}/server/refesh.jpeg'), 'Refresh contact list', self)

        # Config
        self.config_button = QAction(QIcon(f'{BASEDIR}/server/config.jpeg'), 'Config', self)

        # Show history
        self.show_history_button = QAction(QIcon(f'{BASEDIR}/server/history.jpeg'), 'Show history', self)

        # Register new user
        self.register_new_user_button = QAction(QIcon(f'{BASEDIR}/server/add_user.jpg'), 'Register new user', self)

        # Remove user
        self.remove_user_button = QAction(QIcon(f'{BASEDIR}/server/rm_user.jpg'), 'Remove user', self)

        # Statusbar
        # dock widget
        self.statusBar()

        # Toolbar
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_contacts_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.register_new_user_button)
        self.toolbar.addAction(self.remove_user_button)
        self.toolbar.addAction(self.config_button)

        # Main window size.
        self.setFixedSize(800, 600)
        self.setWindowTitle('Chat Server alpha release')

        # Clients list label
        self.label = QLabel('Clients list:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 45)

        # Clients list window
        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 65)
        self.active_clients_table.setFixedSize(780, 400)

        self.show()


class HistoryWindow(QDialog):
    """
    Users history class
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # History window:
        self.setWindowTitle('Users statistic')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Close button
        self.close_button = QPushButton('Close', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        # History table
        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.show()


class ConfigWindow(QDialog):
    """
    Server config class
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Config window
        self.setFixedSize(365, 260)
        self.setWindowTitle('Server config')

        # Database config label:
        self.db_path_label = QLabel('DB file path: ', self)
        self.db_path_label.move(10, 10)
        self.db_path_label.setFixedSize(240, 15)

        # Database file path
        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 30)
        self.db_path.setReadOnly(True)

        # Database select button.
        self.db_path_select = QPushButton('Select...', self)
        self.db_path_select.move(275, 28)

        # File open dialog
        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            # path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        # Database filename label
        self.db_file_label = QLabel('DB filename: ', self)
        self.db_file_label.move(10, 68)
        self.db_file_label.setFixedSize(180, 15)

        # Filename
        self.db_file = QLineEdit(self)
        # self.db_file.setText(DB_FILENAME)
        self.db_file.move(200, 66)
        self.db_file.setFixedSize(150, 20)

        # Port label
        self.port_label = QLabel('Port number:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        # Port
        self.port = QLineEdit(self)
        # self.port.setText(str(system.IP_PORT))
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        # IP label
        self.ip_label = QLabel('Allowed IP:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        # IP
        self.ip = QLineEdit(self)
        # self.ip.setText('0.0.0.0')
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        # Save button
        self.save_btn = QPushButton('Save', self)
        self.save_btn.move(190, 220)

        # Close button
        self.close_button = QPushButton('Close', self)
        self.close_button.move(275, 220)
        self.close_button.clicked.connect(self.close)

        self.show()


def gui_create_model(database: ServerDatabase) -> list:
    """
    Create Qmodel table

    :param database: Server database object
    :return: row list
    """
    list_users = database.get_active_users_list()

    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(['Name', 'IP', 'Port', 'Connection time'])
    for row in list_users:
        user = row.username
        ip = row.ip
        port = row.port
        time = row.time_conn

        user = QStandardItem(user)
        user.setEditable(False)

        ip = QStandardItem(ip)
        ip.setEditable(False)

        port = QStandardItem(str(port))
        port.setEditable(False)

        # Round time to seconds
        time = QStandardItem(str(time.replace(microsecond=0)))
        time.setEditable(False)

        list.appendRow([user, ip, port, time])
    return list


def create_stat_model(database: ServerDatabase) -> list:
    """
    Create messages history counter

    :param database: Server database object
    :return: row list
    """
    hist_list = database.get_message_counter()

    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(
        ['Name', 'Last login', 'Sent', 'Recived']
    )
    for row in hist_list:
        user, last_seen, sent, recvd = row

        user = QStandardItem(user)
        user.setEditable(False)

        last_seen = QStandardItem(str(last_seen.replace(microsecond=0)))
        last_seen.setEditable(False)

        sent = QStandardItem(str(sent))
        sent.setEditable(False)

        recvd = QStandardItem(str(recvd))
        recvd.setEditable(False)

        list.appendRow([user, last_seen, sent, recvd])
    return list


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = MainWindow()
    # ex.statusBar().showMessage('Test Statusbar Message')
    # test_list = QStandardItemModel(ex)
    # test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    # test_list.appendRow([QStandardItem('1'), QStandardItem('2'), QStandardItem('3')])
    # test_list.appendRow([QStandardItem('4'), QStandardItem('5'), QStandardItem('6')])
    # ex.active_clients_table.setModel(test_list)
    # ex.active_clients_table.resizeColumnsToContents()
    # app.exec_()

    app = QApplication(sys.argv)
    message = QMessageBox
    dial = ConfigWindow()  #
    app.exec_()
