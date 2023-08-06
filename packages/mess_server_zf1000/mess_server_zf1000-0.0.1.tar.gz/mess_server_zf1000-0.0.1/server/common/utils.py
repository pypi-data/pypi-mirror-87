from common.variables import *
from common.decos import log
import json
import sys

sys.path.append('../')


# Утилита приёма и декодирования сообщения
# принимает байты выдаёт словарь, если принято что-то другое отдаёт ошибку
# значения
@log
def get_message(client):
    """
    Функция приёма сообщений от удалённых компьютеров. Принимает сообщения JSON, декодирует полученное
    сообщение и проверяет что получен словарь.
    :param client: сокет для передачи данных.
    :return: словарь - сообщение.
    """
    encoded_response = client.recv(
        MAX_PACKAGE_LENGTH)  # recv — получить данные. На входе байты
    # isinstance - возвращает флаг, указывающий на то, является ли указанный объект
    # экземпляром указанного класса
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


# Утилита кодирования и отправки сообщения. Принимает словарь и отправляет его
@log
def send_message(sock, message):
    """
    Функция отправки словарей через сокет. Кодирует словарь в формат JSON и отправляет через сокет.
    :param sock: сокет для передачи
    :param message: словарь для передачи
    :return: ничего не возвращает
    """
    json_message = json.dumps(
        message)    # json.dumps() - метод возвращает строку в формате JSON
    encoded_message = json_message.encode(
        ENCODING)   # из json объекта получаем байты
    sock.send(encoded_message)          # байты шлём по сети
