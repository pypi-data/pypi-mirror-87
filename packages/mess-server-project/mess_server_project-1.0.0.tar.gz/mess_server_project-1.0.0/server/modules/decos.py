"""Декораторы для мессенджера"""
import sys
import logging
import logs.server_log_config
import logs.client_log_config
import traceback
import inspect

if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def logger(log_func):
    """Функция-декоратор, выполняющий логирование вызовов функций."""
    def log_saver(*args, **kwargs):
        """Обертка"""
        res = log_func(*args, **kwargs)
        LOGGER.debug(f'Вызов функции {log_func.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {log_func.__module__}.'
                     f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
        return res
    return log_saver


class Logger:
    """Класс-декоратор, выполняющий логирование вызовов функций."""
    def __call__(self, log_func):
        def log_saver(*args, **kwargs):
            """Обертка"""
            res = log_func(*args, **kwargs)
            LOGGER.debug(f'Была вызвана функция {log_func.__name__} c параметрами {args}, {kwargs}. '
                         f'Вызов из модуля {log_func.__module__}. '
                         f'Вызов из функции {inspect.stack()[1][3]}', stacklevel=2)
            return res
        return log_saver
