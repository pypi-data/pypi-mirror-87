import threading
import logging
import select
from socket import socket, AF_INET, SOCK_STREAM
import json
import hmac
import binascii
import os
from server.server.common.descriptors import Port
from server.server.common.utils import send_message, get_message
#from decorators import login_required


# Загрузка логера
server_logger = logging.getLogger('server')


class MessageProcessor(threading.Thread):
    '''
    Основной класс сервера. Принимает содинения, словари - пакеты
    от клиентов, обрабатывает поступающие сообщения.
    Работает в качестве отдельного потока.
    '''
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        # Параментры подключения
        self.listen_address = listen_address
        self.listen_port = listen_port

        # БД сервера
        self.database = database

        self.sock = None

        # Список подключённых клиентов.
        self.clients = []

        # Сокеты
        self.listen_sockets = None
        self.error_sockets = None

        # Флаг продолжения работы
        self.running = True

        # Словарь содержащий сопоставленные имена и соответствующие им сокеты.
        self.names = dict()

        super().__init__()

    def run(self):
        '''основной цикл потока.'''
        self.init_socket()

        while self.running:
            try:
                client_sock, address = self.sock.accept()
            except OSError:
                pass
            else:
                server_logger.info(f'Установлено соедение  {address}')
                client_sock.settimeout(5)
                self.clients.append(client_sock)

            receive_lst = []
            send_lst = []
            err_lst = []

            try:
                if self.clients:
                    receive_lst, self.listen_sockets, self.error_sockets = \
                        select.select(self.clients, self.clients, [], 0)
            except OSError:
                server_logger.error("Ошибка работы с сокетами")

            # принимаем сообщения и если ошибка, исключаем клиента.
            if receive_lst:
                for client_with_message in receive_lst:
                    try:
                        self.client_requests_handler(
                            get_message(client_with_message), client_with_message)
                    except (OSError, json.JSONDecodeError, TypeError) as err:
                        server_logger.debug(
                            f'Getting data from client exception.', exc_info=err)
                        self.remove_client(client_with_message)

    def remove_client(self, client):
        '''
        обработчик клиента с которым прервана связь.
        Ищет клиента и удаляет его из списков и базы:
        '''
        server_logger.info(
            f'Клиент {client.getpeername()} отключился от сервера.')
        for name in self.names:
            if self.names[name] == client:
                self.database.logout(name)
                del self.names[name]
                break
        self.clients.remove(client)
        client.close()

    def init_socket(self):
        '''Инициализация сокета'''
        server_logger.info(
            f'Сервер запущен.'
            f'Адрес и порт :  {self.listen_port}, {self.listen_address} '
            f'Если адрес не указан, принимаются соединения с любых адресов.')

        # создаем сокет
        server_sock = socket(AF_INET, SOCK_STREAM)
        server_sock.bind((self.listen_address, self.listen_port))
        server_sock.settimeout(3)

        self.sock = server_sock
        self.sock.listen(5)

    def process_message(self, message):
        '''Отправка сообщения клиенту.'''
        if message['to'] in self.names and self.names[message['to']
                                                      ] in self.listen_sockets:
            try:
                send_message(self.names[message['to']], message)
                server_logger.info(
                    f'Отправлено сообщение пользователю {message["to"]} от пользователя {message["from"]}.')
            except OSError:
                self.remove_client(message["to"])
        elif message["to"] in self.names and self.names[message["to"]] not in self.listen_sockets:
            server_logger.error(
                f'Связь с клиентом {message["to"]} была потеряна. Соединение закрыто, доставка невозможна.')
            self.remove_client(self.names[message["to"]])
        else:
            server_logger.error(
                f'Пользователь {message["to"]} не зарегистрирован на сервере, отправка сообщения невозможна.')

    # @login_required
    def client_requests_handler(self, message, client):
        """
        Валидация сообщения от клиента и
        отправка ответа сервера
        """

        server_logger.debug(f'Сообщение : {message} клиента {client}')
        # обрабатываем сообщение присутствие и регистрация пользователя
        if 'action' in message and message['action'] == 'presence' and 'time' in message \
                and 'user' in message:
            server_logger.debug(f"Принято и обработано presence сообщение")
            self.autorize_user(message, client)

        # если есть сообщение - то отправляем получателю
        elif 'action' in message and message['action'] == 'message' and 'time' in message \
                and 'message_text' in message and 'to' in message and 'from' in message \
                and self.names[message['from']] == client:
            server_logger.debug(
                f"Принято сообщение --- > проверка пользователя -- > отправка получателю")
            if message['to'] in self.names:
                self.database.count_messages(message['from'], message['to'])
                self.process_message(message)
                try:
                    send_message(client, {'response': 200})
                except OSError:
                    self.remove_client(client)
            else:
                response = {'response': 400, 'error': None}
                response['error'] = 'Пользователь не зарегистрирован на сервере.'
                try:
                    send_message(client, response)
                except OSError:
                    pass
            return

        # если клиент выходит
        elif 'action' in message and message['action'] == 'exit' and 'account_name' in message and \
                self.names[message['account_name']] == client:
            self.remove_client(client)

        # запрос списка контактов
        elif 'action' in message and message['action'] == 'get_contacts' and 'user' in message and \
                self.names[message['user']] == client:
            response = {'response': 202,
                        'data_list': None}

            response['data_list'] = self.database.get_contacts(message['user'])
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # добавление контакта
        elif 'action' in message and message['action'] == 'add' and 'account_name' in message and 'user' in message \
                and self.names[message['user']] == client:
            self.database.add_contact(message['user'], message['account_name'])
            try:
                send_message(client, {"response": 200})
            except OSError:
                self.remove_client(client)

        # удаление контакта
        elif 'action' in message and message['action'] == 'remove' and 'account_name' in message and 'user' in message \
                and self.names[message['user']] == client:
            self.database.remove_contact(
                message['user'], message['account_name'])
            try:
                send_message(client, {"response": 200})
            except OSError:
                self.remove_client(client)

        # запрос списка всех пользователей
        elif 'action' in message and message['action'] == 'get_users' and 'account_name' in message \
                and self.names[message['account_name']] == client:
            response = {'response': 202,
                        'data_list': None}
            response['data_list'] = [user[0]
                                     for user in self.database.users_list()]
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

        # запрос публичного ключа пользователя
        elif 'action' in message and message['action'] == 'pubkey_need' and 'account_name' in message:
            response = {'response': 511, 'bin': None}
            response['bin'] = self.database.get_pubkey(message['account_name'])
            # может быть, что ключа ещё нет (пользователь никогда не логинился,
            # тогда шлём 400)
            if response['bin']:
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)
            else:
                response = {"response": 400, "error": None}
                response["error"] = 'Нет публичного ключа для данного пользователя'
                try:
                    send_message(client, response)
                except OSError:
                    self.remove_client(client)

        else:
            response = {"response": 400, "error": None}
            response["error"] = 'Bad Request'
            try:
                send_message(client, response)
            except OSError:
                self.remove_client(client)

    def autorize_user(self, message, sock):
        '''Авторизация пользователя'''

        server_logger.debug(f'Start auth process for {message["user"]}')
        if message["user"]['account_name'] in self.names.keys():
            response = {"response": 400, "error": None}
            response["error"] = 'Имя пользователя уже занято.'
            server_logger.debug(f"Имя пользователя уже занято.")
            try:
                server_logger.debug(f'Username busy, sending {response}')
                send_message(sock, response)
            except OSError:
                server_logger.debug('OS Error')
                pass
            self.clients.remove(sock)
            sock.close()
        # Если пользователь не зарегистрирован - отправляем 400 ошибку
        elif not self.database.check_user(message["user"]['account_name']):
            server_logger.debug(
                f"Пользователь : {message['user']['account_name']}не зарегистрирован.")
            response = {"response": 400, "error": None}
            response["error"] = 'Пользователь не зарегистрирован.'
            try:
                send_message(sock, response)
                server_logger.debug(f'Unknown username, sending {response}')
            except OSError:
                pass
            self.clients.remove(sock)
            server_logger.debug(
                f"Пользователь удален из списка потенциальных клиентов")
            sock.close()
        else:
            server_logger.debug('Correct username, starting password check.')
            message_auth = {'response': 511, 'bin': None}

            random_str = binascii.hexlify(os.urandom(64))
            message_auth['bin'] = random_str.decode('ascii')
            hash = hmac.new(
                self.database.get_hash(
                    message["user"]['account_name']),
                random_str,
                'MD5')
            digest = hash.digest()
            server_logger.debug(f'Auth message = {message_auth}')
            try:
                send_message(sock, message_auth)
                ans = get_message(sock)
            except OSError as err:
                server_logger.debug('Error in auth, data:', exc_info=err)
                sock.close()
                return
            client_digest = binascii.a2b_base64(ans['bin'])
            # Если ответ клиента корректный, то сохраняем его в список
            # пользователей.
            if 'response' in ans and ans['response'] == 511 and hmac.compare_digest(
                    digest, client_digest):
                self.names[message["user"]['account_name']] = sock
                client_ip, client_port = sock.getpeername()
                server_logger.debug(
                    f"Ответ клиента корректный - клиент сохранен в список пользователей")
                try:
                    send_message(sock, {"response": 200})
                except OSError:
                    self.remove_client(message["user"]['account_name'])
                # добавляем пользователя в список активных и если у него изменился открытый ключ
                # сохраняем новый
                self.database.login(
                    message["user"]['account_name'],
                    client_ip,
                    client_port,
                    message['user']['pubkey'])
            else:
                response = {"response": 400, "error": None}
                response["error"] = 'Неверный пароль.'
                try:
                    send_message(sock, response)
                except OSError:
                    pass
                self.clients.remove(sock)
                sock.close()

    def service_update_lists(self):
        '''Отправка 205 сообщения'''
        for client in self.names:
            try:
                send_message(self.names[client], {"response": 205})
            except OSError:
                self.remove_client(self.names[client])
