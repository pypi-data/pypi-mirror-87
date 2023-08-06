from common.variables import LOGGING_LEVEL
import logging
import sys
import os
sys.path.append('../')

# создаём формировщик логов (formatter):
client_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
# os.path.abspath(path) - возвращает нормализованный абсолютный путь
# os.path.dirname(path) - возвращает имя директории пути path
# __file__ - это путь к файлу, из которого загружен модуль
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client_logs/client.log')

# создаём потоки вывода логов
# создаём обработчик, который выводит сообщения в поток (в консоль) stderr
# в консоль будут выводится ERROR и CRITICAL
steam = logging.StreamHandler(sys.stderr)
# подключаем объект Formatter к обработчику
steam.setFormatter(client_formatter)
steam.setLevel(logging.INFO)           # установим уровень логгера

log_file = logging.FileHandler(path, encoding='utf8')   # вывод записи в файл
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('client')
# добавим обработчик к регистратору
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
