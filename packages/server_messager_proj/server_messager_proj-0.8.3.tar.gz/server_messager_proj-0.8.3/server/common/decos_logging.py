import logging
import os
from datetime import datetime
import inspect


if os.getcwd().split('/')[-1].split('.')[0] == 'client':
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        LOGGER.debug(f"Обращение к функции : {func.__name__} с аргументами {args} {kwargs}."
                     f"Функция {func.__name__} была вызвана : {datetime.now().strftime('%d-%m-%Y %H:%M')}"
                     f" из функции {inspect.stack()[1][3]}")
        return result
    return wrapper


class Log:
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            LOGGER.debug(f"Обращение к функции : {func.__name__} с аргументами {args} {kwargs}."
                         f"Функция {func.__name__} была вызвана : {datetime.now().strftime('%d-%m-%Y %H:%M')}"
                         f" из функции {inspect.stack()[1][3]}")
            return result
        return wrapper



