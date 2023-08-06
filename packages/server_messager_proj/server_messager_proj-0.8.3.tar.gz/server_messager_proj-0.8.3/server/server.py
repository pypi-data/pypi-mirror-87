import argparse
import os
import sys
import logging
import configparser
from server.server.common.decos_logging import log
from PyQt5.QtWidgets import QApplication
from server.server.server.core import MessageProcessor
from server.server.server.server_db import ServerStorage
from server.server.server.server_gui import MainWindow
from PyQt5.QtCore import Qt


#-p 8079 -a 95.161.221.138

server_logger = logging.getLogger('server')


@log
def arg_parser(default_port, default_address):
    """Чтение аргументов с командной строки при запуске скрипта"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default=default_address, nargs='?')
    parser.add_argument('-p', default=default_port, type=int, nargs='?')
    parser.add_argument('--no_gui', action='store_true')
    args = parser.parse_args()
    address = args.a
    port = args.p
    gui_flag = args.no_gui

    server_logger.info('Аргументы успешно загружены')
    return address, port, gui_flag

@log
def config_load():
    """Загрузка настроек из ini файла"""
    config = configparser.ConfigParser()
    dir_path = os.path.dirname(os.getcwd())
    config.read(f"{dir_path}/{'server.ini'}")

    if 'SETTINGS' in config:
        return config
    else:
        config.add_section('SETTINGS')
        config.set('SETTINGS', 'Default_port', str(7777))
        config.set('SETTINGS', 'Listen_Address', '')
        config.set('SETTINGS', 'Database_path', '')
        config.set('SETTINGS', 'Database_file', 'chat_bd.db')
        return config


def main():
    config = config_load()

    # Загрузка параметров командной строки
    listen_address, listen_port, gui_flag = arg_parser(config['SETTINGS']['Default_port'],
                                                        config['SETTINGS']['Listen_Address'])

    # Инициализация базы данных
    database = ServerStorage(os.path.join(config['SETTINGS']['Database_path'], config['SETTINGS']['Database_file']))

    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    if gui_flag:
        while True:
            command = input('Введите exit для завершения работы сервера.')
            if command == 'exit':
                server.running = False
                server.join()
                break

    else:
        # графическое окуружение для сервера:
        server_app = QApplication(sys.argv)
        server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        main_window = MainWindow(database, server, config)

        # Запускаем GUI
        server_app.exec_()

        server.running = False



if __name__ == '__main__':
    main()
