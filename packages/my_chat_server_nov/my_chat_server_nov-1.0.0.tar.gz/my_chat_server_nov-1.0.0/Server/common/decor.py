from sys import argv, path
import socket
import logging
import logs.client_log_config
import logs.server_log_config
from inspect import stack
path.append('../')
# выбор логгера
if argv[0].find('client') == -1:
    LOG = logging.getLogger('server')
else:
    LOG = logging.getLogger('client')


# #####################  func()  ############################
def log(x):
    """
    Декоратор логирования. Передает в лог сервера или клиента название модуля, название функции и её аргументы.
    """
    def my_saver(*args, **kwargs):
        LOG.debug(f'Была вызвана функция {x.__name__},'
                  f' из модуля {x.__module__},'
                  f' с аргументами: {args}, {kwargs}', stacklevel=2)
        y = x(*args, **kwargs)
        return y
    return my_saver


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере.
    Проверяет, что передаваемый объект сокета находится в
    списке авторизованных клиентов.
    За исключением передачи словаря-запроса
    на авторизацию. Если клиент не авторизован,
    генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from common.const import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    # Проверяем, что данный сокет есть в списке names класса
                    # MessageProcessor
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True

            # Теперь надо проверить, что передаваемые аргументы не presence
            # сообщение. Если presense, то разрешаем
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            # Если не не авторизован и не сообщение начала авторизации, то
            # вызываем исключение.
            if not found:
                raise TypeError
        return func(*args, **kwargs)
    return checker
