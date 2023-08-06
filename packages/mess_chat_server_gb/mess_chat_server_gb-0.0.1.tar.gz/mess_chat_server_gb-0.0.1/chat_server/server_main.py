"""
A module to run the chat server application.
"""

import json
import os
import sys
from json import JSONDecodeError

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer

from server.server_database import ServerDatabase
from server import server_gui
from server.server_core import ChatServerCore
from server.register_new_user import RegisterNewUser
from server.remove_user import RemoveUser
from common.cpypt import ChatCrypting

BASEDIR = os.getcwd()


def main() -> None:
    """
    The function gets the configuration from command line arguments or configuration files.
     Initializes all application components and passes the resulting configuration to them.
    :return: None
    """
    try:
        with open(
                file=f'{BASEDIR}/common/config/config.json',
                encoding='utf-8',
                mode='r'
        ) as c_file:
            config = json.load(c_file)
    except (FileNotFoundError, JSONDecodeError):
        config = {
            "port": 7777,
            "address": '0.0.0.0',
            "db_path": '',
            "db_file": 'server_db.sqlite3'
        }

    # Инициализация базы данных
    database = ServerDatabase(
        db_path=os.path.join(
            config.get("db_path"),
            config.get("db_file")
        )
    )

    # Создание экземпляра класса - сервера и его запуск:
    server_core = ChatServerCore(
        address=config.get("address"),
        port=config.get("port"),
        database=database,
        crypt=ChatCrypting
    )
    server_core.daemon = True
    server_core.start()

    # Создаём графическое окуружение для сервера:
    server_app = QApplication(sys.argv)
    main_window = server_gui.MainWindow()

    # Инициализируем параметры в окна
    main_window.statusBar().showMessage('Server Working')
    main_window.active_clients_table.setModel(server_gui.gui_create_model(database))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    # Функция обновляющяя список подключённых, проверяет флаг подключения, и
    # если надо обновляет список
    def list_update():
        main_window.active_clients_table.setModel(
            server_gui.gui_create_model(database)
        )
        main_window.active_clients_table.resizeColumnsToContents()
        main_window.active_clients_table.resizeRowsToContents()

    # Функция создающяя окно со статистикой клиентов

    def show_statistics():
        global stat_window
        stat_window = server_gui.HistoryWindow()
        stat_window.history_table.setModel(
            server_gui.create_stat_model(database)
        )
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    # Функция создающяя окно с настройками сервера.
    def server_config():
        global config_window
        # Создаём окно и заносим в него текущие параметры
        config_window = server_gui.ConfigWindow()
        config_window.db_path.insert(config.get("db_path"))
        config_window.db_file.insert(config.get("db_file"))
        config_window.port.insert(str(config.get("port")))
        config_window.ip.insert(config.get("address"))
        config_window.save_btn.clicked.connect(save_server_config)

    # Функция сохранения настроек
    def save_server_config():
        global config_window
        message = QMessageBox()
        config["db_path"] = config_window.db_path.text()
        config["db_file"] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
        else:
            config["address"] = config_window.ip.text()
            if 1023 < port < 65536:
                config["port"] = str(port)

                with open(
                        file=f'{BASEDIR}/common/config/config.json',
                        encoding='utf-8',
                        mode='w'
                ) as c_file:
                    c_file.write(json.dumps(config, ensure_ascii=False))

                    message.information(config_window, 'OK', 'Настройки успешно сохранены!')
            else:
                message.warning(
                    config_window,
                    'Ошибка',
                    'Порт должен быть от 1024 до 65536'
                )

    def register_new_user():
        global register_window
        register_window = RegisterNewUser(database=database, server=server_core)
        register_window.show()

    def remove_user():
        global remove_window
        remove_window = RemoveUser(database=database, server=server_core)
        remove_window.show()

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    # Связываем кнопки с процедурами
    main_window.refresh_contacts_button.triggered.connect(list_update)
    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_button.triggered.connect(server_config)
    main_window.register_new_user_button.triggered.connect(register_new_user)
    main_window.remove_user_button.triggered.connect(remove_user)

    # Запускаем GUI
    server_app.exec_()


if __name__ == '__main__':
    main()
