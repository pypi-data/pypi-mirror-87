from logging import handlers, StreamHandler, getLogger, ERROR
from sys import path as system_path, stderr
from os import path, getcwd
system_path.append(path.join(getcwd(), '..'))
from common.const import LOG_LVL, SERVER_FORMAT, SERVER_PATH, SERVER_LOG_NAME


PATH = path.dirname(path.abspath(__file__))
PATH = path.join(PATH, SERVER_PATH, SERVER_LOG_NAME)

STREAM = StreamHandler(stderr)
STREAM.setFormatter(SERVER_FORMAT)
STREAM.setLevel(ERROR)

LOGS = handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='D')
LOGS.setFormatter(SERVER_FORMAT)

LOG = getLogger('server')
LOG.addHandler(STREAM)
LOG.addHandler(LOGS)
LOG.setLevel(LOG_LVL)

# if __name__ == '__main__':
#     LOG.critical('Критическая ошибка')
#     LOG.error('Ошибка')
#     LOG.debug('Отладочная информация')
#     LOG.info('Информационное сообщение')
