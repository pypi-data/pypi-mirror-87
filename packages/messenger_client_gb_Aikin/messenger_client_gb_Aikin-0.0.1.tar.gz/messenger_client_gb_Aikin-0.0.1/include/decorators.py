""" Декораторы """
import inspect
import sys
import traceback

from log_configs import client_log_config #, server_log_config

# if sys.argv[0].find('client') > 0:
#    logger = client_log_config.get_logger()
# else:
#    logger = server_log_config.get_logger()

logger = client_log_config.get_logger()

def log(func):
    """Функция-декоратор логирования функции"""
    def wrapper(*args, **kwargs):
        logger.debug(f'Вызывается функция: [{func.__name__}] c аргументами ({args}{kwargs})\n'
                     f'Функция вызывается из функции [{inspect.stack()[1].function}]\n'
                     f'Логирование декоратором-функцией!')
        res = func(*args, **kwargs)
        # logger.debug(f'Конец вызова')
        return res

    return wrapper


class Log:
    """Класс-декоратор логирования функции"""
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            logger.debug(f'Вызывается функция: [{func.__name__}] c аргументами ({args}{kwargs})\n'
                         f'Функция вызывается из функции [{traceback.format_stack()[0].split()[-1]}]\n'
                         f'Логирование декоратором-классом')
            res = func(*args, **kwargs)
            return res
        return wrapper
