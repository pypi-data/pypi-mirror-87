import sys
import logging

from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
sys.path.append('../')

LOGGER = logging.getLogger('client')


class AddContactWindow(QDialog):
    """
    Окно добавления в список контактов.
    """
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database

        self.setFixedSize(350, 120)
        self.setWindowTitle('Выберите пользователя для добавления:')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите пользователя для добавления:', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.btn_refresh = QPushButton('Обновить список', self)
        self.btn_refresh.setFixedSize(100, 30)
        self.btn_refresh.move(60, 60)

        self.btn_add = QPushButton('Добавить', self)
        self.btn_add.setFixedSize(100, 30)
        self.btn_add.move(230, 20)

        self.btn_cancel = QPushButton('Отмена', self)
        self.btn_cancel.setFixedSize(100, 30)
        self.btn_cancel.move(230, 60)
        self.btn_cancel.clicked.connect(self.close)

        self.contacts_update()

        self.btn_refresh.clicked.connect(self.contacts_update)

    def contacts_update(self):
        """
        Функция создает список всех зарегистрированных пользователей
        за исключением уже добавленных в контакты и самого себя.
        """
        self.selector.clear()

        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        """
        Функция для обновления списка возможных контактов.
        Запрос данных сервера для обновления содержимого окна.
        """
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            LOGGER.debug('Обновление списка пользователей прошло успешно')
            self.contacts_update()
