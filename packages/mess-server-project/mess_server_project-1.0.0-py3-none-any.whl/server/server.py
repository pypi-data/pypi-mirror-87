"""Сервер"""
import os
import sys
import logging
import configparser

from modules.decos import logger
from server.server_database import ServerStorage
from server.core import Server
from server.main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

LOGGER = logging.getLogger('server')


@logger
def main():
    """
    Функция определения параметров и запуска сервера
    :return:
    """
    config = configparser.ConfigParser()

    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")

    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = config['SETTINGS']['Default_port']

    except IndexError:
        LOGGER.critical(f'Попытка запуска сервера без указания порта.')
        sys.exit(1)
    except ValueError:
        LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = config['SETTINGS']['Listen_Address']
    except IndexError:
        print('Для установки адреса введите число в формате "-a 127.0.0.1"')
        sys.exit(1)

    database = ServerStorage(os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))
    server = Server(address, port, database)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(database, server, config)

    server_app.exec_()

    server.running = False


if __name__ == '__main__':
    main()


