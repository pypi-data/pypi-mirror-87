import argparse
import os
import sys

from Crypto.PublicKey import RSA
from PyQt5.QtWidgets import QApplication, QMessageBox

import logs.config.config_client_log
from client.database import ClientDatabase
from client.main_window import ClientMainWindow
from client.start_dialog import UserNameDialog
from client.transport import ClientTransport
from common.decos import log
from common.errors import ServerError
from common.variables import *

# Инициализация логера
logger = logging.getLogger('client')


# Парсер аргументов коммандной строки
@log
def arg_parser():
    """
        Парсер аргументов командной строки, возвращает кортеж из 4 элементов
        адрес сервера, порт, имя пользователя, пароль.
        Выполняет проверку на корректность номера порта.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    # Проверка подходящего номера порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name, client_passwd


# Основная функция клиента
if __name__ == '__main__':
    # Загрузка параметров коммандной строки
    server_address, server_port, client_name, client_passwd = arg_parser()
    logger.debug('Args loaded')

    # Создание клиентского приложения
    client_app = QApplication(sys.argv)

    # Запрос имени пользователя, если его не было в командной строке
    start_dialog = UserNameDialog()
    if not client_name or not client_passwd:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_passwd = start_dialog.client_passwd.text()
            logger.debug(
                f'Using USERNAME = {client_name}, PASSWD = {client_passwd}.')
        else:
            exit(0)

    # Запись логов
    logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, имя пользователя: {client_name}')

    # Загрузка ключей с файла, иначе создание новой пары
    dir_path = os.path.dirname(os.path.realpath(__file__))
    key_file = os.path.join(dir_path, f'{client_name}.key')
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    keys.publickey().export_key()

    logger.debug("Загрузка ключей успешно завершена")
    # Создание объекта базы данных
    database = ClientDatabase(client_name)
    # Создание объекта - транспорта и запуск транспортного потока
    try:
        transport = ClientTransport(
            server_port,
            server_address,
            database,
            client_name,
            client_passwd,
            keys)
        logger.debug("Transport ready.")
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    # Удаление объекта диалога
    del start_dialog

    # Создание GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат *demo_version* - {client_name}')
    client_app.setStyleSheet(style)
    client_app.exec_()

    # Закрытие транспорта
    transport.transport_shutdown()
    transport.join()
