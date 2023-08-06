import logging.handlers
import os
import sys

from common.variables import LOGGING_LEVEL

sys.path.append('../')

# Создание формировщика логов (formatter)
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, '../logs/server.log')

# Создание потоков вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(logging.INFO)
log_file = logging.handlers.TimedRotatingFileHandler(
    path, encoding='utf8', interval=1, when='D')
log_file.setFormatter(server_formatter)

# Создание и настройка регистратора
logger = logging.getLogger('server')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)
