"""Клиентское приложение"""
import os
import sys
import argparse

from Cryptodome.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

from modules.variables import *
from modules.decos import logger
from client.client_database import ClientDatabase
from client.transport import ClientTransport
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog

LOGGER = logging.getLogger('client')


@logger
def arg_parser():
    '''
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов
    адрес сервера, порт, имя пользователя, пароль.
    Выполняет проверку на корректность номера порта.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    if not 1023 < server_port < 65536:
        LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535.'
            f' Клиент завершается.')
        sys.exit(1)

    return server_address, server_port, client_name, client_passwd


if __name__ == '__main__':
    server_address, server_port, client_name, client_passwd = arg_parser()
    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
        else:
            sys.exit(0)

    LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , '
        f'порт: {server_port}, имя пользователя: {client_name}')

    dir_path = os.getcwd()
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    database = ClientDatabase(client_name)

    try:
        sock = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        LOGGER.debug("Transport ready.")
    except Exception as err:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', str(err))
        sys.exit(1)

    sock.setDaemon(True)
    sock.start()

    del start_dialog

    main_window = ClientMainWindow(database, sock, keys)
    main_window.make_connection(sock)
    main_window.setWindowTitle(f'Клиент-мессенджер - {client_name}')
    client_app.exec_()

    sock.transport_shutdown()
    sock.join()
