import binascii
import hashlib
import hmac
import socket
import sys
import time
import logging
import json
import threading

from PyQt5.QtCore import pyqtSignal, QObject
from modules.functions import *
from modules.variables import *


sys.path.append('../')
LOGGER = logging.getLogger('client')
socket_lock = threading.Lock()


class ClientTransport(threading.Thread, QObject):
    """
    Класс реализующий транспортную подсистему клиентского
    модуля. Отвечает за взаимодействие с сервером.
    """
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        threading.Thread.__init__(self)
        QObject.__init__(self)

        self.database = database
        self.username = username
        self.password = passwd
        self.transport = None
        self.keys = keys
        self.connection_init(port, ip_address)

        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                LOGGER.critical(f'Потеряно соединение с сервером.')
            LOGGER.error('Таймаут соединения при обновлении списков пользователей.')
        except json.JSONDecodeError:
            LOGGER.critical(f'Потеряно соединение с сервером.')

        self.running = True

    def connection_init(self, port, ip):
        """Метод для установки соединения с сервером."""
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.transport.settimeout(5)

        connected = False
        for i in range(5):
            LOGGER.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except(OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                LOGGER.debug('Соединение установлено.')
                break
            time.sleep(1)

        if not connected:
            LOGGER.critical('Не удалось установить соединение с сервером')
            raise Exception('Не удалось установить соединение с сервером')

        LOGGER.debug('Запуск аутентификации.')

        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes, salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        LOGGER.debug(f'Хэш пароля готов: {passwd_hash_string}')

        pubkey = self.keys.publickey().export_key().decode('ascii')

        with socket_lock:
            presence = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            LOGGER.debug(f'Сообщение присутствия = {presence}')

            try:
                send_message(self.transport, presence)
                ans = get_message(self.transport)
                LOGGER.debug(f'Ответ сервера = {ans}')
                if RESPONSE in ans:
                    if ans[RESPONSE] == 400:
                        raise Exception(f'{ans[ERROR]}')
                    elif ans[RESPONSE] == 511:
                        ans_data = ans[DATA]
                        hash = hmac.new(passwd_hash_string, ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = RESPONSE_511
                        my_ans[DATA] = binascii.b2a_base64(digest).decode('ascii')
                        send_message(self.transport, my_ans)
                        self.parse_server_ans(get_message(self.transport))
            except (OSError, json.JSONDecodeError):
                LOGGER.critical('Потеряно соединение с сервером')
                raise Exception('Потеряно соединение с сервером!')

    def parse_server_ans(self, message):
        """Метод для обработки поступающих сообщений с сервера."""
        LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise Exception(f'{message[ERROR]}')
            elif message[RESPONSE] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                LOGGER.error(f'Принят неизвестный код подтверждения {message[RESPONSE]}')

        elif ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and message[DESTINATION] == self.username:
            LOGGER.debug(f'Получено сообщение от пользователя {message[SENDER]}:{message[MESSAGE_TEXT]}')
            self.new_message.emit(message)

    def contacts_list_update(self):
        """Метод для обновелния с сервера списка контактов."""
        LOGGER.debug(f'Запрос контакт листа для пользователся {self.name}')
        request = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        LOGGER.debug(f'Сформирован запрос {request}')
        with socket_lock:
            send_message(self.transport, request)
            answer = get_message(self.transport)
        LOGGER.debug(f'Получен ответ {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            for contact in answer[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            LOGGER.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        """Метод для обновления с сервера списка пользователей."""
        LOGGER.debug(f'Запрос списка известных пользователей {self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT: self.username
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            LOGGER.error('Не удалось обновить список известных пользователей.')

    def add_contact(self, contact):
        """Метод для отправки сведений на сервер о добавлении контакта."""
        LOGGER.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.parse_server_ans(get_message(self.transport))

    def remove_contact(self, contact):
        """Метод для отправки сведений на сервер об удалении контакта."""
        LOGGER.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.parse_server_ans(get_message(self.transport))

    def transport_shutdown(self):
        """Метод для уведомления сервера о завершении работы клиента."""
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT: self.username
        }
        with socket_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                pass
        LOGGER.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def key_request(self, user):
        """Метод запрашивающий с сервера публичный ключ пользователя."""
        LOGGER.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT: user
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if RESPONSE in ans and ans[RESPONSE] == 511:
            return ans[DATA]
        else:
            LOGGER.error(f'Не удалось получить ключ для собеседника {user}')

    def send_message(self, to, message):
        """Метод для отправки сообщений на сервер."""
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')

        with socket_lock:
            send_message(self.transport, message_dict)
            self.parse_server_ans(get_message(self.transport))
            LOGGER.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        """Метод содержащий основной цикл работы транспортного потока."""
        LOGGER.debug('Запущен прием сообщений')
        while self.running:
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        LOGGER.critical(f'Потеряно соединение с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError, TypeError):
                    LOGGER.debug('Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.transport.settimeout(5)

            if message:
                LOGGER.debug(f'Принято сообщение от сервера: {message}')
                self.parse_server_ans(message)
