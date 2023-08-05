"""Утилиты"""

import json
from modules.variables import MAX_PACKAGE_LEN, ENCODING


def send_message(sock, message):
    """
    Функция приема словаря, кодирования и отправки сообщения
    :param sock:
    :param message:
    :return:
    """

    json_message = json.dumps(message)
    result_message = json_message.encode(ENCODING)
    sock.send(result_message)


def get_message(client):
    """
    Функция приема сообщения и декодирование его в словарь
    :param client:
    :return:
    """

    response = client.recv(MAX_PACKAGE_LEN)
    if isinstance(response, bytes):
        json_response = response.decode(ENCODING)
        dict_response = json.loads(json_response)
        if isinstance(dict_response, dict):
            return dict_response
        raise ValueError
    raise ValueError
