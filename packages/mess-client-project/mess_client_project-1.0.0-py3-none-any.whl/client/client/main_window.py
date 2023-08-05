import sys
import json
import logging
import base64

from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox, QApplication, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from modules.variables import *
from client.client_window import Ui_MainWindow
from client.add_contact import AddContactWindow
from client.delete_contact import DelContactWindow
from client.client_database import ClientDatabase
from client.transport import ClientTransport
from client.start_dialog import UserNameDialog

sys.path.append('../')


LOGGER = logging.getLogger('client')


class ClientMainWindow(QMainWindow):
    """
    Основное окно пользовательского приложения.
    Конфигурация окна создана в QTDesigner и загружается из
    конвертированого файла client_window.py
    """
    def __init__(self, database, transport, keys):
        super().__init__()
        self.database = database
        self.transport = transport
        self.decrypter = PKCS1_OAEP.new(keys)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.menu_2.triggered.connect(qApp.exit)

        self.ui.btn_send_msg.clicked.connect(self.send_message)

        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.action.triggered.connect(self.add_contact_window)

        self.ui.btn_delete_contact.clicked.connect(self.delete_contact_window)
        self.ui.action_2.triggered.connect(self.delete_contact_window)

        self.ui.menu_2.triggered.connect(qApp.quit)
        self.contacts_model = None
        self.history_model = None
        self.messages = QMessageBox()
        self.current_chat = None
        self.current_chat_key = None
        self.encryptor = None
        self.ui.list_dialog.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_dialog.setWordWrap(True)

        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.clients_list_update()
        self.set_disabled_input()
        self.show()

    def set_disabled_input(self):
        """Метод делает поля ввода неактивными"""
        self.ui.text_field_msg.clear()
        if self.history_model:
            self.history_model.clear()
        self.ui.btn_send_msg.setDisabled(True)
        self.ui.text_field_msg.setDisabled(True)

    def history_list_update(self):
        """
        Метод заполняющий диалог историей переписки с текущим собеседником.
        """
        list = sorted(self.database.get_history(self.current_chat), key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_dialog.setModel(self.history_model)
        self.history_model.clear()
        length = len(list)
        start_idx = 0
        if length > 20:
            start_idx = length - 20
        for i in range(start_idx, length):
            item = list[i]
            if item[1] == 'in':
                msg = QStandardItem(f'Входящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                msg.setEditable(False)
                msg.setBackground(QBrush(QColor(255, 213, 213)))
                msg.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(msg)
            else:
                msg = QStandardItem(f'Исходящее от {item[3].replace(microsecond=0)}:\n {item[2]}')
                msg.setEditable(False)
                msg.setTextAlignment(Qt.AlignRight)
                msg.setBackground(QBrush(QColor(204, 255, 204)))
                self.history_model.appendRow(msg)
        self.ui.list_dialog.scrollToBottom()

    def select_active_user(self):
        """Метод обработчик события двойного клика по списку контактов."""
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        """Метод активации чата с собеседником."""
        try:
            self.current_chat_key = self.transport.key_request(self.current_chat)
            LOGGER.debug(f'Загружен открытый ключ для {self.current_chat}')
            if self.current_chat_key:
                self.encryptor = PKCS1_OAEP.new(RSA.import_key(self.current_chat_key))
        except (OSError, json.JSONDecodeError):
            self.current_chat_key = None
            self.encryptor = None
            LOGGER.debug(f'Не удалось получить ключ для {self.current_chat}')

        if not self.current_chat_key:
            self.messages.warning(self, 'Ошибка', 'Для выбранного пользователя нет ключа шифрования.')
            return

        self.ui.label_dialog.setText(f'Диалог с {self.current_chat}')
        self.ui.btn_send_msg.setDisabled(False)
        self.ui.text_field_msg.setDisabled(False)

        self.history_list_update()

    def clients_list_update(self):
        """Метод обновляющий список контактов."""
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for i in sorted(contacts_list):
            item = QStandardItem(i)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def add_contact_window(self):
        """Метод вызывающий окно - диалог добавления контакта."""
        global select_dialog
        select_dialog = AddContactWindow(self.transport, self.database)
        select_dialog.btn_add.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        """Метод обработчк нажатия кнопки 'Добавить'."""
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        """
        Метод добавляет контакт в серверную и клиентсткую базу данных.
        После обновления баз данных обновляет и содержимое окна.
        """
        try:
            self.transport.add_contact(new_contact)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            LOGGER.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успех', 'Контакт успешно добавлен.')

    def delete_contact_window(self):
        """Метод создающий окно удаления контакта."""
        global remove_dialog
        remove_dialog = DelContactWindow(self.database)
        remove_dialog.btn_ok.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, item):
        """Метод удаляющий контакт из серверной и клиентсткой базы данных."""
        selected = item.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            LOGGER.info(f'Успешно удалён контакт {selected}')
            self.messages.information(self, 'Успех', 'Контакт успешно удалён.')
            item.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def send_message(self):
        """
        Функция отправки сообщения текущему собеседнику.
        Реализует шифрование сообщения и его отправку.
        """
        msg_text = self.ui.text_field_msg.toPlainText()
        self.ui.text_field_msg.clear()
        if not msg_text:
            return
        message_text_encrypted = self.encryptor.encrypt(msg_text.encode('utf-8'))
        message_text_encrypted_base64 = base64.b64encode(message_text_encrypted)
        try:
            self.transport.send_message(self.current_chat, message_text_encrypted_base64.decode('ascii'))
            pass
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
                self.close()
            print(err)
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения!')
        except (ConnectionResetError, ConnectionAbortedError):
            self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером!')
            self.close()
        else:
            self.database.save_message(self.current_chat, 'out', msg_text)
            LOGGER.debug(f'Отправлено сообщение для {self.current_chat}: {msg_text}')
            self.history_list_update()

    @pyqtSlot(dict)
    def message(self, message):
        """
        Слот обработчик поступаемых сообщений, выполняет дешифровку
        поступаемых сообщений и их сохранение в истории сообщений.
        Запрашивает пользователя если пришло сообщение не от текущего
        собеседника. При необходимости меняет собеседника.
        """
        encrypted_message = base64.b64decode(message[MESSAGE_TEXT])
        try:
            decrypted_message = self.decrypter.decrypt(encrypted_message)
        except (ValueError, TypeError):
            self.messages.warning(self, 'Ошибка', 'Не удалось декодировать сообщение.')
            return

        self.database.save_message(self.current_chat, 'in', decrypted_message.decode('utf8'))

        sender = message[SENDER]
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}, открыть чат с ним?', QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    self.current_chat = sender
                    self.set_active_user()
            else:
                print('NO')
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n Данного пользователя нет в '
                                          f'вашем контакт-листе.\n Добавить в контакты и открыть чат с ним?',
                                          QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        """
        Слот обработчик потери соеднинения с сервером.
        Выдаёт окно предупреждение и завершает работу приложения.
        """
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером. ')
        self.close()

    @pyqtSlot()
    def sig_205(self):
        """Слот выполняющий обновление баз данных по команде сервера."""
        if self.current_chat and not self.database.check_user(self.current_chat):
            self.messages.warning(self, 'Ошибка', 'Собеседник удален с сервера')
            self.set_disabled_input()
            self.current_chat = None
        self.clients_list_update()

    def make_connection(self, trans_obj):
        """Метод для соединения сигналов и слотов."""
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)
        trans_obj.message_205.connect(self.sig_205)
