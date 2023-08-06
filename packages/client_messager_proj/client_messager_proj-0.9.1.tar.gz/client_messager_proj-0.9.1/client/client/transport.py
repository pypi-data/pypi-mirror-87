from server.server.common.utils import get_message, send_message
from socket import socket, AF_INET, SOCK_STREAM
import time
import logging
import json
import threading
import hashlib
import hmac
import binascii
from PyQt5.QtCore import pyqtSignal, QObject


# логгер
client_logger = logging.getLogger('client')
# объект блокировки сокета
socket_lock = threading.Lock()


class ClientConnection(threading.Thread, QObject):
    """Класс - взаимодействие с сервером"""

    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, password, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.username = username
        self.password = password
        self.client_sock = None
        self.keys = keys
        self.connection_init(port, ip_address)
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError:
            client_logger.error(
                'Timeout соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            client_logger.critical(f'Потеряно соединение с сервером.')
            raise Exception('Потеряно соединение с сервером!')
        # флаг продолжение работы сокета
        self.running = True

    def connection_init(self, port, ip):
        """Инициализация соединения"""
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.settimeout(10)

        connected = False
        for i in range(5):
            client_logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.client_sock.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                client_logger.debug(
                    f"ошибка при попытке соединения - client_sock.connect")
                pass
            else:
                connected = True
                client_logger.debug("Connection established")
                break
            time.sleep(1)

        if not connected:
            client_logger.critical(
                'Не удалось установить соединение с сервером')
            raise Exception('Не удалось установить соединение с сервером')

        client_logger.debug('Установлено соединение с сервером')

        # получаем хэш пароль
        password_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        password_hash = hashlib.pbkdf2_hmac(
            'sha512', password_bytes, salt, 10000)
        password_hash_str = binascii.hexlify(password_hash)

        client_logger.debug(f'Password hash ready: {password_hash_str}')

        # публичный ключ
        pubkey = self.keys.publickey().export_key().decode('ascii')
        client_logger.debug(f"Публичный ключ готов : {pubkey}")

        # авторизация

        with socket_lock:
            presence = {
                'action': 'presence',
                'time': time.time(),
                'user': {
                    'account_name': self.username,
                    'pubkey': pubkey
                }
            }
            client_logger.debug(f"Presence message = {presence}")

            try:
                send_message(self.client_sock, presence)
                answer = get_message(self.client_sock)
                client_logger.debug(f'Server response = {answer}.')

                if 'response' in answer:
                    if answer['response'] == 400:
                        client_logger.critical(
                            f"400 ответ сервера - ошибка : {answer['error']}")
                    elif answer['response'] == 511:
                        answer_data = answer['bin']
                        hash_ = hmac.new(
                            password_hash_str, answer_data.encode('utf-8'), 'MD5')
                        digest = hash_.digest()
                        my_answer = {'response': 511, 'bin': None}
                        my_answer['bin'] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.client_sock, my_answer)
                        self.server_response_handler(
                            get_message(self.client_sock))
            except (OSError, json.JSONDecodeError) as err:
                client_logger.debug(f'Connection error.', exc_info=err)
                raise ConnectionError

    def create_presence(self):
        """Формируем сообщение присутствия"""
        result = {
            'action': 'presence',
            'time': time.time(),
            'user': {
                'account_name': self.username
            }
        }
        client_logger.info(
            f'Сформировано "presence" сообщение для пользователя {self.username}')
        return result

    def server_response_handler(self, message):
        """Обработка сообщения-присутствия сервера"""
        client_logger.debug(f'Разбор сообщения от сервера: {message}')
        if 'response' in message:
            if message['response'] == 200:
                return '200 : OK'
            elif message['response'] == 400:
                return f'400 : {message["error"]}'
            elif message['response'] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                client_logger.error(
                    f'Принят неизвестный код подтверждения {message["response"]}')

        elif 'action' in message and message['action'] == 'message' and 'from' in message and 'to' in message \
             and 'message_text' in message and message['to'] == self.username:
            client_logger.debug(
                f'Получено сообщение от пользователя {message["from"]}:{message["message_text"]}')
            self.new_message.emit(message)

    def contacts_list_update(self):
        '''Метод обновляющий с сервера список контактов.'''
        self.database.contacts_clear()
        client_logger.debug(
            f'Запрос контакт листа для пользователя {self.name}')
        request = {
            'action': 'get_contacts',
            'time': time.time(),
            'user': self.username
        }
        client_logger.debug(f'Сформирован запрос {request}')
        with socket_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        client_logger.debug(f'Получен ответ {answer}')
        if 'response' in answer and answer['response'] == 202:
            for contact in answer['data_list']:
                self.database.add_contact(contact)
        else:
            client_logger.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        client_logger.debug(f'Запрос списка пользователей {self.username}')
        request = {
            'action': 'get_users',
            'time': time.time(),
            'account_name': self.username
        }
        with socket_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        if 'response' in answer and answer['response'] == 202:
            self.database.add_users(answer['data_list'])
        else:
            client_logger.error(
                'Не удалось обновить список известных пользователей.')

    def add_contact(self, contact):
        """Добавление контакта"""
        client_logger.debug(f'Создание контакта {contact}')
        request = {
            'action': 'add',
            'time': time.time(),
            'user': self.username,
            'account_name': contact
        }
        with socket_lock:
            send_message(self.client_sock, request)
            self.server_response_handler(get_message(self.client_sock))

    def remove_contact(self, contact):
        """Удаление контакта"""
        client_logger.debug(f'Удаление контакта {contact}')
        request = {
            'action': 'remove',
            'time': time.time(),
            'user': self.username,
            'account_name': contact
        }
        with socket_lock:
            send_message(self.client_sock, request)
            self.server_response_handler(get_message(self.client_sock))

    def transport_shutdown(self):
        """Уведомление о завершении работы клиента"""
        self.running = False
        message = {
            'action': 'exit',
            'time': time.time(),
            'account_name': self.username
        }
        with socket_lock:
            try:
                send_message(self.client_sock, message)
            except OSError:
                pass
        client_logger.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def key_request(self, user):
        '''Метод запрашивающий с сервера публичный ключ пользователя.'''
        client_logger.debug(f'Запрос публичного ключа для {user}')
        request = {
            'action': 'pubkey_need',
            'time': time.time(),
            'account_name': user
        }
        with socket_lock:
            send_message(self.client_sock, request)
            answer = get_message(self.client_sock)
        if 'response' in answer and answer['response'] == 511:
            return answer['bin']
        else:
            client_logger.error(f'Не удалось получить ключ собеседника{user}.')

    def send_message(self, to_user, message):
        """Отправка сообщения пользователю"""
        message_dict = {
            'action': 'message',
            'from': self.username,
            'to': to_user,
            'time': time.time(),
            'message_text': message
        }
        client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')

        with socket_lock:
            send_message(self.client_sock, message_dict)
            self.server_response_handler(get_message(self.client_sock))
            client_logger.info(
                f'Отправлено сообщение для пользователя {to_user}')

    def run(self):
        """Основной цикл работы потока"""
        client_logger.debug('Запущен процесс - приёмник собщений с сервера.')
        while self.running:
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.client_sock.settimeout(0.5)
                    message = get_message(self.client_sock)
                except OSError as err:
                    if err.errno:
                        client_logger.critical(
                            f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    client_logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.client_sock.settimeout(5)

            if message:
                client_logger.debug(f'Принято сообщение с сервера: {message}')
                self.server_response_handler(message)
