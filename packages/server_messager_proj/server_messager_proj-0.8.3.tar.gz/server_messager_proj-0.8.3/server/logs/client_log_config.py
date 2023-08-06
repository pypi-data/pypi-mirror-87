import logging.handlers
import os
import sys

sys.path.append('../../../')

# путь к папке с фалом
PATH = os.path.join(os.getcwd(), 'log_files/client.log')

# создаем объект форматирования
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# параметры логов (путь, формат, уровень, ротация)
SYSTEM_HANDLER = logging.StreamHandler(sys.stderr)
SYSTEM_HANDLER.setFormatter(CLIENT_FORMATTER)
SYSTEM_HANDLER.setLevel(logging.ERROR)
FILE_TO_LOGGING = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
FILE_TO_LOGGING.setFormatter(CLIENT_FORMATTER)

# создание логов
LOG_OBJ = logging.getLogger('client')
LOG_OBJ.addHandler(SYSTEM_HANDLER)
LOG_OBJ.addHandler(FILE_TO_LOGGING)
LOG_OBJ.setLevel(logging.DEBUG)

if __name__ == '__main__':
    LOG_OBJ.critical('Crtical error')
    LOG_OBJ.error('Error')
    LOG_OBJ.debug('Debug information')
    LOG_OBJ.info('Info message')

