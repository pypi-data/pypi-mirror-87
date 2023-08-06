import argparse
import os
import sys
sys.path.append('../../../')
import logging
from Crypto.PublicKey import RSA
from server.server.common.decos_logging import log
from client.client.client.client_db import ClientStorage
from PyQt5.QtWidgets import QApplication, QMessageBox
from client.client.client.transport import ClientConnection
from client.client.client.main_window_gui import ClientMainWindow
from client.client.client.start_dialog import UserNameDialog


#-p 8079 -a 95.161.221.138

client_logger = logging.getLogger('client')

@log
def arg_parser():
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default="127.0.0.1", nargs='?')
    parser.add_argument('port', default=7777, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    args = parser.parse_args(sys.argv[1:])
    address = args.addr
    port = args.port
    name = args.name
    password = args.password

    if port < 1023 and port > 65536:
        client_logger.critical(
            f'Ошибка.Недопустимый порт'
            f'{port}.Порт должен быть в диапазоне от 1024 до 65536')
        sys.exit(1)

    return address, port, name, password



if __name__ == '__main__':
    server_address, server_port, client_name, client_password = arg_parser()
    client_logger.debug('Load arguments')

    client_app = QApplication(sys.argv)

    start_dialog = UserNameDialog()

    # запрашиваем имя пользователя
    if not client_name or not client_password:
        client_app.exec_()

        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_password = start_dialog.client_passwd.text()
            client_logger.debug(f'Using USERNAME = {client_name}, PASSWD = {client_password}.')
        else:
            sys.exit(0)

    client_logger.info(
        f'Запущен клиент: адрес сервера: {server_address} , порт: {server_port}, имя пользователя: {client_name}')

    #  загрузка ключей из файла
    dir_path = os.path.dirname(os.getcwd())
    key_file = os.path.join(dir_path, f'{client_name}.key')

    # если ключ файл с ключем не найден - генерируем новую пару ключей
    if not os.path.exists(key_file):
        keys = RSA.generate(2048, os.urandom)
        with open(key_file, 'wb') as key:
            key.write(keys.export_key())
    else:
        with open(key_file, 'rb') as key:
            keys = RSA.import_key(key.read())

    client_logger.debug("Keys sucsessfully loaded.")


    try:
        database = ClientStorage(client_name)
        client_logger.debug(f"Создан объект базы данных клиента {client_name}")
    except Exception as err:
        print(f"Ошибка {err}")
        client_logger.critical(f"Ошибка создания объекта базыд данных клиента {err}")

    try:
        transport = ClientConnection(server_port, server_address, database, client_name, client_password, keys)
        client_logger.debug("Transport ready.")
    except Exception:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка сервера')
        sys.exit(1)

    transport.setDaemon(True)
    transport.start()

    del start_dialog

    # GUI
    main_window = ClientMainWindow(database, transport, keys)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Чат - {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()



