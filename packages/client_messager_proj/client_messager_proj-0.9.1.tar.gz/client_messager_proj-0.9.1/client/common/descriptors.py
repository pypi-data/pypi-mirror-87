import logging
import sys

LOGGER = logging.getLogger('server')

class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            LOGGER.critical(
            f'Ошибка.Недопустимый порт'
            f'{value}.Порт должен быть в диапазоне от 1024 до 65536')
            sys.exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name