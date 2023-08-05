"""Конфигурация для логирования клиентского приложения"""

import sys
import os
import logging
from modules.variables import LOGGING_LEVEL

# Регистратор
LOGGER = logging.getLogger('client')

# Формат вывода сообщения
FORMATTER = logging.Formatter(
    '%(asctime)s %(filename)s %(levelname)s %(message)s')

# Формирование пути сохранения логов
PATH = os.getcwd()
PATH = os.path.join(PATH, "client_logs", "client.log")

# Потоки вывода логов
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOGGING_FILE = logging.FileHandler(PATH, encoding='utf8')
LOGGING_FILE.setFormatter(FORMATTER)


# Настройка регистратора
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOGGING_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')