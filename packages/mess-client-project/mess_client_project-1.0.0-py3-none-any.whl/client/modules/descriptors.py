import logging
import sys

LOGGER = logging.getLogger('server')


class Port:
    """
    Класс-дескриптор для номера порта.
    Позволяет использовать только порты с 1023 по 65536.
    При попытке установить неподходящий номер порта генерирует исключение.
    """

    def __set__(self, instance, value):
        if int(value) < 1024 or int(value) > 65535:
            LOGGER.critical(
                f'Попытка запуска сервера с указанием неподходящего порта.')
            sys.exit(1)
        instance.__dict__[self.name] = int(value)

    def __set_name__(self, owner, name):
        self.name = name
