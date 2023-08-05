from logging import FileHandler, StreamHandler, getLogger, ERROR
from sys import path as system_path, stderr
from os import path, getcwd
system_path.append(path.join(getcwd(), '..'))
from common.const import LOG_LVL, CLIENT_FORMAT, CLIENT_PATH, CLIENT_LOG_NAME


PATH = path.dirname(path.abspath(__file__))
PATH = path.join(PATH, CLIENT_PATH, CLIENT_LOG_NAME)

STREAM = StreamHandler(stderr)
STREAM.setFormatter(CLIENT_FORMAT)
STREAM.setLevel(ERROR)

LOGS = FileHandler(PATH, encoding='utf8')
LOGS.setFormatter(CLIENT_FORMAT)

LOG = getLogger('client')
LOG.addHandler(STREAM)
LOG.addHandler(LOGS)
LOG.setLevel(LOG_LVL)

# if __name__ == '__main__':
#     LOG.critical('Критическая ошибка')
#     LOG.error('Ошибка')
#     LOG.debug('Отладочная информация')
#     LOG.info('Информационное сообщение')
