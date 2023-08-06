import socket
import logging
import logs.config_client_log
import logs.config_server_log
import sys

sys.path.append('../')

# метод определения модуля, источника запуска.
# Метод find () возвращает индекс первого вхождения искомой подстроки,
# если он найден в данной строке.
# Если его не найдено, - возвращает -1.
# sys.argv - содержит полный путь к скрипту или к названию файла
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


# Реализация в виде функции
def log(func):
    """
    Декоратор, выполняющий логирование вызовов функций. Сохраняет события типа debug, содержащие информацию
    о имени вызываемой функиции, параметры с которыми вызывается функция, и модуль, вызывающий функцию.
    """
    def wrap_log(*args, **kwargs):
        """Обертка"""
        logger.debug(
            f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
            f'Вызов из модуля {func.__module__}')
        res = func(*args, **kwargs)
        return res
    return wrap_log


def login_required(func):
    """
    Декоратор, проверяющий, что клиент авторизован на сервере. Проверяет, что передаваемый
    объект сокета находится в списке авторизованных клиентов. За исключением передачи
    словаря-запроса на авторизацию. Если клиент не авторизован, генерирует исключение TypeError
    """

    def checker(*args, **kwargs):
        # проверяем, что первый аргумент - экземпляр MessageProcessor
        # Импортить необходимо тут, иначе ошибка рекурсивного импорта.
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
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


# Реализация в виде класса
# class Log:
#     """Класс-декоратор"""
#     def __call__(self, func):
#         def wrap_log(*args, **kwargs):
#             """Обертка"""
#             res = func(*args, **kwargs)
#             LOGGER.debug(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}. '
#                          f'Вызов из модуля {func.__module__}. Вызов из'
#                          f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
#                          f'Вызов из функции {inspect.stack()[1][3]}')
#             return res
#         return wrap_log
