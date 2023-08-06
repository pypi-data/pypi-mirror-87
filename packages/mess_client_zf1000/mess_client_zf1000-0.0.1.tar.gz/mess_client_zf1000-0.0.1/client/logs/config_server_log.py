from common.variables import LOGGING_LEVEL
import os
import logging.handlers
import logging
import sys
sys.path.append('../')

# создаём формировщик логов (formatter):
server_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'server_logs/server.log')

# создаём потоки вывода логов
steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(server_formatter)
steam.setLevel(logging.INFO)
# when='d' - тип нтервала (день)
# interval=1 - интервал времени (через день)
# ежедневная ротация лог-файлов
log_file = logging.handlers.TimedRotatingFileHandler(
    path, encoding='utf8', interval=1, when='d')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('server')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
