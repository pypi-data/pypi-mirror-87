import sys
from socket import socket, AF_INET, SOCK_STREAM
import hashlib
import select

from common.external_func import send_msg_finish, get_message
from common.vars import DEF_PORT, DEF_IP, EXIT, ACTION, TIME, ACCOUNT_NAME, MESSAGE, SENDER, \
    DESTINATION, MESSAGE_TEXT, USER, ERROR, RESPONCE_400, GET_CONTACT, ADD_CONTACT, USER_ID_TO_CONTACT, \
    RESPONCE_202, \
    CUSTOM_RESPONCE, RESPONCE, DATA, REGISTER, PASSWORD_HASH, RESPONCE_511, RESPONCE_ERROR, LOGIN_REQUEST
import argparse

from metaclass import ServerMaker
from descrptrs import Port
from db_class_server import ServerStorage


# Парсер аргументов командной строки
def arg_parce():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEF_PORT)
    parser.add_argument('-a', default=DEF_IP, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


# Главный класс Сервера
class ServerClass(metaclass=ServerMaker):
    '''
        Основной класс сервера
    '''
    port = Port()

    def __init__(self, listen_address, listen_port, database):
        self.addr = listen_address
        self.port = listen_port
        self.database = database
        self.all_clients = []
        self.name = dict()
        self.message = []

    # Создание транспортного сокета
    def create_socket(self):
        '''
        Созданисе транспортного сокета
        '''
        srv_transport = socket(AF_INET, SOCK_STREAM)
        srv_transport.bind((self.addr, self.port))
        srv_transport.settimeout(0.5)

        self.socket = srv_transport
        self.socket.listen()

    # Главный цикл работы
    def mainlopp(self):
        '''
         Главный цикл сервера.
         Создает очереди получения и отправки сообщений
        '''
        self.create_socket()
        try:
            while True:
                try:
                    client, client_address = self.socket.accept()
                except Exception:
                    pass
                else:
                    print(f'Получен запрос на соединение.{client_address}')
                    self.all_clients.append(client)

                recv_data_lst = []
                send_data_lst = []
                err_lst = []
                try:
                    if self.all_clients:
                        recv_data_lst, send_data_lst, err_lst = select.select(self.all_clients, self.all_clients, [], 0)
                except Exception:
                    pass

                # Прием сообщений
                if recv_data_lst:
                    for client_with_message in recv_data_lst:
                        try:
                            self.process_client_message(get_message(client_with_message), client_with_message)

                            # принимаем сообщения
                        except Exception:
                            self.all_clients.remove(client_with_message)

                for message in self.message:
                    try:
                        # print('Process_message try')
                        self.process_message(message, send_data_lst)
                    except Exception:
                        self.all_clients.remove(self.name[message[DESTINATION]])
                        del self.name[message[DESTINATION]]
                self.message.clear()
        except Exception:
            pass

    # Функция обработки ответа от пользователя
    def process_client_message(self, message, client):
        '''
        Функция обработки ответа от пользователя.

        '''

        # Регистрация пользователя
        if ACTION in message and message[ACTION] == REGISTER and TIME in message and USER in message:
            print('---')
            client_ip, client_port = client.getpeername()
            user = message[USER][ACCOUNT_NAME]
            password = message[USER][PASSWORD_HASH]
            password = password.encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac('sha256', password, user.encode('utf-8'), 100000)
            print('Password hash - ', password_hash)
            print('Username -- ', user)

            register = self.database.user_register(username=user, ip_address=client_ip, port=client_port,
                                                   hash_passwod=password_hash)
            if register == True:
                send_msg_finish(client, RESPONCE_511)
            else:
                RESPONCE_ERROR[RESPONCE] = 512
                RESPONCE_ERROR[ERROR] = 'Пользователь уже зарегистрирован'
                send_msg_finish(client, RESPONCE_ERROR)


        # Логин пользователя
        elif ACTION in message and message[ACTION] == LOGIN_REQUEST:
            print('Account login Request')
            self.name[message[USER][ACCOUNT_NAME]] = client
            client_ip, client_port = client.getpeername()
            user = message[USER][ACCOUNT_NAME]
            password = message[USER][PASSWORD_HASH]
            password = password.encode('utf-8')
            password_hash = hashlib.pbkdf2_hmac('sha256', password, user.encode('utf-8'), 10000)
            print('Password hash - ', password_hash)
            print('Username -- ', user)
            login_user = self.database.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port,
                                                  password_hash=password_hash)
            if login_user == True:
                responce = RESPONCE_400
                responce[RESPONCE] = 515
                responce[ERROR] = ''
                print('Senf msg to client login true')
                send_msg_finish(client, responce)
            if login_user == False:
                responce = RESPONCE_400
                responce[RESPONCE] = 516
                responce[ERROR] = 'Неправильный логин - пароль'
                print('Senf msg to client login false')
                send_msg_finish(client, responce)
                self.all_clients.remove(client)
                client.clse()

        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            self.message.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.database.user_logout(message[ACCOUNT_NAME])
            self.all_clients.remove(self.name[ACCOUNT_NAME])
            self.name[ACCOUNT_NAME].close()
            del self.name[ACCOUNT_NAME]
            return
        # Запрос контак листа
        elif ACTION in message and message[ACTION] == GET_CONTACT and SENDER in message:
            self.database.contact_list(message[SENDER])
            print('Запрос контакт листа ----')
            print('----')
            RESPONCE_202[RESPONCE] = 202
            RESPONCE_202[DATA] = self.database.contact_list(message[SENDER])
            print('-----')
            send_msg_finish(client, RESPONCE_202)
            print('----')


        # Добавление в контакт лист
        elif ACTION in message and message[
            ACTION] == ADD_CONTACT and SENDER in message and USER_ID_TO_CONTACT in message:
            print('Запрос на добавление в контакт лист')
            self.database.add_contact(message[SENDER], message[USER_ID_TO_CONTACT])
            print('---')
            CUSTOM_RESPONCE[RESPONCE] = 500
            CUSTOM_RESPONCE[DATA] = 'OK'
            print(CUSTOM_RESPONCE)
            send_msg_finish(client, CUSTOM_RESPONCE)
            print('-------')
            # send_msg_finish(client, RESPONCE_200)

        else:
            response = RESPONCE_400
            response[ERROR] = 'Запрос некорректен'
            send_msg_finish(client, response)

    # Функиця отправки сообщения Пользователь - Пользователь
    def process_message(self, message, listen_socket):
        if message[DESTINATION] in self.name and self.name[message[DESTINATION]] in listen_socket:
            send_msg_finish(self.name[message[DESTINATION]], message)
            print(f'Отправлено сообщение пользователю {message[DESTINATION]} от {message[SENDER]}')
        else:
            print(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере')


# Функция при старте приложения
def main():
    '''
        Стартовые действия при запуске сервера.

    '''
    database = ServerStorage()
    listen_address, listen_port = arg_parce()
    server = ServerClass(listen_address, listen_port, database)
    # server.daemon = True
    # server.start()
    server.mainlopp()


if __name__ == '__main__':
    main()
