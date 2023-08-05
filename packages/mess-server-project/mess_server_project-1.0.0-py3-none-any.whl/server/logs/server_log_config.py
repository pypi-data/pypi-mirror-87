"""Конфигурация для логирования сервера"""

import sys
import os
import logging
import logging.handlers
from modules.variables import LOGGING_LEVEL
sys.path.append('../')


LOGGER = logging.getLogger('server')

PATH = os.getcwd()
PATH = os.path.join(PATH, 'server_logs', 'server.log')

FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)

LOG_FILE_HANDLER = logging.handlers.TimedRotatingFileHandler(
    PATH, encoding='utf8', interval=1, when='D')
LOG_FILE_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
