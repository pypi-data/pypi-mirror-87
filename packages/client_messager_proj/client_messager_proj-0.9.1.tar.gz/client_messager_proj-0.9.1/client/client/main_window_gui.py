from client.client.client.del_contact import DelContactDialog
from client.client.client.contact_add import AddContactDialog
from client.client.client.client_gui import Ui_MainClientWindow
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, Qt
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64
import sys
import json
import logging

sys.path.append('../../../')

client_log = logging.getLogger('client')


class ClientMainWindow(QMainWindow):
    """
    Класс основного окна пользователя.
    Окно создано в QTDesigner и загружено из
    файла client_gui.py
    """

    def __init__(self, database, transport, keys):
        super().__init__()

        self.database = database
        self.transport = transport

        # объект - дешифорвщик сообщений
        self.decrypter = PKCS1_OAEP.new(keys)

        # Загрузка настроек окна из дизайнера
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        # Кнопка "Выход"
        self.ui.menu_exit.triggered.connect(qApp.exit)

        # Кнопка "отправить сообщение"
        self.ui.btn_send.clicked.connect(self.send_message)

        # кнопка "добавить контакт"
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)

        # кнопка "Удалить контакт"
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)

        # дополнительный константы экземпляра класса
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_messages.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        # Даблклик
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        ''' Метод делающий поля ввода неактивными'''
        self.ui.label_new_message.setText(
            'Для выбора получателя дважды кликните на нем в окне контактов.')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

        self.encryptor = None
        self.current_chat = None
        self.current_chat_key = None

    def history_list_update(self):
        """История сообщений"""
        list = sorted(
            self.database.get_history(
                self.current_chat),
            key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)

        self.history_model.clear()
        length = len(list)
        start_index = 0
        # берем максимум 20 последних записей
        if length > 20:
            start_index = length - 20

        for i in range(start_index, length):
            item = list[i]
            if item[1] == 'in':
                mess = QStandardItem(
                    f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setBackground(QBrush(QColor(255, 213, 213)))
                mess.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(mess)
            else:
                mess = QStandardItem(
                    f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                mess.setEditable(False)
                mess.setTextAlignment(Qt.AlignRight)
                mess.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(mess)
        self.ui.list_messages.scrollToBottom()

    def select_active_user(self):
        """Обработчик даблклика по контакту"""
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """Функция устанавливающяя активного собеседника"""
        try:
            self.current_chat_key = self.transport.key_request(
                self.current_chat)
            client_log.debug(f'Загружен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(
                    RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            client_log.debug(
                f'Не удалось получить ключ для {self.current_chat}')

        # Если ключа нет то ошибка, что не удалось начать чат с пользователем
        if not self.current_chat_key:
            self.messages.warning(
                self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return

        self.ui.label_new_message.setText(
            f'Введите сообщенние для пользователя {self.current_chat}:')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)

        self.history_list_update()

    def clients_list_update(self):
        """Обновление списка контактов"""
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """Добавление контакта"""
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database)
        select_dialog.btn_ok.clicked.connect(
            lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """Обработка добавления, обновления списка контактов"""
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """Добавление контакта в БД"""
        try:
            self.transport.add_contact(new_contact)
        except Exception:
            self.messages.critical(self, 'Ошибка сервера')
        except OSError:
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            client_log.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(
                self, 'Успех', 'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """Удаление контакта"""
        global remove_dialog
        remove_dialog = DelContactDialog(self.database)
        remove_dialog.btn_ok.clicked.connect(
            lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """Обработчик адление контакта, обновление списка контактов"""
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except Exception:
            self.messages.critical(self, 'Ошибка сервера')
        except OSError:
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            client_log.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()

            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """Отправка сообщения пользователю"""
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return

        message_text_encrypted = self.encryptor.encrypt(
            message_text.encode('utf8'))
        message_text_encrypted_base64 = base64.b64encode(
            message_text_encrypted)

        try:
            self.transport.send_message(
                self.current_chat,
                message_text_encrypted_base64.decode('ascii'))
            pass
        except Exception:
            self.messages.critical(self, 'Ошибка')
        except OSError:
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(
                self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(self.current_chat, 'out', message_text)
            client_log.debug(
                f'Отправлено сообщение для {self.current_chat}: {message_text}')
            self.history_list_update()

    @pyqtSlot(dict)
    def message(self, message):
        """Слот приёма нового сообщений"""

        encrypted_message = base64.b64decode(message['message_text'])

        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(
                self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return

        self.database.save_message(
            self.current_chat,
            'in',
            decrypted_message.decode('utf8'))

        sender = message['from']
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(
                    self,
                    'Новое сообщение',
                    f'Получено новое сообщение от {sender}, открыть чат с ним?',
                    QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                print('NO')
                if self.messages.question(
                    self,
                    'Новое сообщение',
                    f'Получено новое сообщение от {sender}.\n'
                    f'Данного пользователя нет в вашем контакт-листе.\n'
                    f'Добавить в контакты и открыть чат с ним?',
                    QMessageBox.Yes,
                        QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.database.save_message(
                        self.current_chat, 'in', decrypted_message.decode('utf8'))
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """Потеря соединения"""
        self.messages.warning(
            self,
            'Сбой соединения',
            'Потеряно соединение с сервером. ')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        '''
        Слот выполняющий обновление баз данных по команде сервера.
        '''
        if self.current_chat and not self.database.check_user(
                self.current_chat):
            self.messages.warning(
                self,
                'Сочувствую',
                'К сожалению собеседник был удалён с сервера.')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_list_update()

    def make_connection(self, trans_obj):
        '''Соединение сигналов и слотов.'''
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)
        trans_obj.message_205.connect(self.sig_205)
