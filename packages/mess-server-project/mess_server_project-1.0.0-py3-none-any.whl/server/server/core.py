import threading
import logging
import select
import socket
import json
import hmac
import binascii
import os

from modules.metaclasses import ServerMaker
from modules.descriptors import Port
from modules.variables import *
from modules.functions import send_message, get_message


LOGGER = logging.getLogger('server')


class Server(threading.Thread):
    """
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    """
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port

        self.database = database

        self.sock = None

        self.clients = []

        self.listen_sockets = None
        self.error_sockets = None

        self.running = True
        self.names = dict()

        super().__init__()

    def run(self):
        """Основной цикл потока"""
        self.socket_init()

        while self.running:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                LOGGER.info(f'Установлено соединение с ПК {client_address}')
                client.settimeout(5)
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, self.listen_sockets, self.error_sockets = \
                        select.select(self.clients, self.clients, [], 0)
            except OSError as err:
                LOGGER.error(f'Ошибка работы с сокетами: {err.errno}')

            if recv_data_lst:
                for client_with_msg in recv_data_lst:
                    try:
                        self.parse_client_message(get_message(client_with_msg), client_with_msg)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        LOGGER.debug(f'Ошибка', exc_info=err)
                        self.remove_client(client_with_msg)

    def remove_client(self, client):
        """
        Метод обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы.
        """
        LOGGER.info(f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.user_logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def socket_init(self):
        """Метод инициализации сокета"""
        LOGGER.info(f'Запущен сервер, порт для подключений: {self.port}, '
                    f'адрес с которого принимаются подключения: {self.addr}. '
                    f'Если адрес не указан, принимаются соединения с любых адресов.')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.addr, self.port))
        sock.settimeout(0.5)

        self.sock = sock
        self.sock.listen(MAX_CON)

    def transfer_message(self, message):
        """
        Функция отправляет сообщения определенному клиенту.
        :param message:
        :return:
        """
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in self.listen_sockets:
            try:
                send_message(self.names[message[DESTINATION]], message)
                LOGGER.info(f'Отправлено сообщение от пользователя {message[SENDER]} '
                            f'пользователю {message[DESTINATION]}.')
            except OSError:
                self.remove_client(message[DESTINATION])
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in self.listen_sockets:
            LOGGER.error(
                f'Связь с клиентом {message[DESTINATION]} была потеряна. Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message[DESTINATION]])
        else:
            LOGGER.error(
                f'Пользователь {message[DESTINATION]} не зарегистрирован, '
                f'отправка сообщения невозможна.')

    def parse_client_message(self, message, client):
        """
        Метод-обработчик поступающих сообщений
        :param message:
        :param client:
        """

        LOGGER.debug(f'Проверка сообщения от клиента : {message}')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            self.user_authorization(message, client)

        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message and self.names[message[SENDER]] == client:
            if message[DESTINATION] in self.names:
                self.database.marking_message(message[SENDER], message[DESTINATION])
                self.transfer_message(message)
                try:
                    send_message(client, RESPONSE_200)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT in message \
                and self.names[message[ACCOUNT]] == client:
            self.remove_client(client)

        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message \
                and self.names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = self.database.get_contacts(message[USER])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.add_contact(message[USER], message[ACCOUNT])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT in message and USER in message \
                and self.names[message[USER]] == client:
            self.database.remove_contact(message[USER], message[ACCOUNT])
            try:
                send_message(client, RESPONSE_200)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT in message \
                and self.names[message[ACCOUNT]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT])
            if response[DATA]:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Публичный ключ для данного пользователся отсутствует'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)

        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректен.'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def user_authorization(self, message, sock):
        """Метод для авторизации пользователя."""
        LOGGER.debug(f'Процесс аутентификации для пользователя {message[USER]}')
        if message[USER][ACCOUNT] in self.names.keys():
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя занято.'
            try:
                LOGGER.debug(f'Имя пользователя занято, отправка {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        elif not self.database.check_user(message[USER][ACCOUNT]):
            response = RESPONSE_400
            response[ERROR] = 'Пользователь не зарегистрирован.'
            try:
                LOGGER.debug(f'Неизвестный пользователь: {response}')
                send_message(sock, response)
            except OSError:
                pass
            self.clients.remove(sock)
            sock.close()
        else:
            LOGGER.debug('Проверка пароля')
            response = RESPONSE_511
            random_str = binascii.hexlify(os.urandom(64))
            response[DATA] = random_str.decode('ascii')

            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT]), random_str, 'MD5')
            digest = hash.digest()

            LOGGER.debug(f'Сообщение авторизации = {response}')
            try:
                send_message(sock, response)
                answer = get_message(sock)
            except OSError as err:
                LOGGER.debug('Ошибка аутентификации:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(answer[DATA])

            if RESPONSE in answer and answer[RESPONSE] == 511 and hmac.compare_digest(digest, client_digest):
                self.names[message[USER][ACCOUNT]] = sock
                client_ip, client_port = sock.getpeername()
                try:
                    send_message(sock, RESPONSE_200)
                except OSError:
                    self.remove_client(message[USER][ACCOUNT])

                self.database.user_login(message[USER][ACCOUNT], client_ip, client_port, message[USER][PUBLIC_KEY])
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неправильный пароль'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        """Метод для отправки сервисного сообщения 205 клиентам."""
        for client in self.names:
            try:
                send_message(self.names[client], RESPONSE_205)
            except OSError:
                self.remove_client(self.names[client])
