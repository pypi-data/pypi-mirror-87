from logging import getLogger
from sys import argv
import logs.client_log_config
import logs.server_log_config


if argv[0].find('client') == -1:
    LOG = getLogger('server')
else:
    LOG = getLogger('client')


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            LOG.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535.')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
