import socket
import sys
from common.vars import DEF_PORT, DEF_IP, EXIT, ACTION, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, \
    PRESENCE, USER, ERROR, RESPONCE, DEF_IP_ADDRES_FOR_CLIENT, GET_CONTACT, ADD_CONTACT, DEL_CONTACT, \
    USER_ID_TO_CONTACT, \
    CUSTOM_RESPONCE, MSG_RESP, DATA, REGISTER, PASSWORD_HASH, LOGIN_REQUEST
import argparse
import select
import time
import threading
import argparse
from common.external_func import send_msg_finish, get_message
from metaclass import ClientMaker
from metaclass import Dis_test
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QListWidgetItem
# from PyQt5.QtCore import pyqtSignal, QObject
# from chat_gui_ver2 import MainWindow


class ClientSenderClass(threading.Thread):

    def __init__(self, account_name, socket):
        self.account = account_name
        self.socket = socket
        super().__init__()

    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account
        }

    def create_message(self):
        to = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        print(message_dict)
        try:
            send_msg_finish(self.socket, message_dict)
        except:
            exit(1)
    # Получения списка контактов
    def get_contact(self):
        message_dict = {
            ACTION: GET_CONTACT,
            SENDER: self.account,
            TIME: time.time(),
        }
        print('get_contact')
        return message_dict

    def add_contact(self, contact):
        message_dict = {
            ACTION: ADD_CONTACT,
            SENDER: self.account,
            USER_ID_TO_CONTACT: contact,
            TIME: time.time(),
        }
        return message_dict

    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_msg_finish(self.socket, self.create_exit_message())
                except:
                    pass
                print("Завершение соединения")
                time.sleep(0.5)
                break
            elif command == 'list':
                try:
                    send_msg_finish(self.socket, self.get_contact())
                except:
                    print('Ошибка сообщения получения контактов')
            elif command == 'add_contact':
                contact = input('Введите имя контакт: ')
                try:
                    send_msg_finish(self.socket, self.add_contact(contact))
                except:
                    print('Ошибка отправки добавления в контакты')
            else:
                print('Команда не распознана. Введите help')

    def print_help(self):
        print('------')
        print('message - отправить сообщение. Кому и текст сообщения отдельно')
        print('help - вывести подсказки по командам')
        print('exit - выход ')
        print('list - для получения контактов')
        print('add_contact - для добавления контакта')
        print('------')


class ClientReaderClass(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, socket):
        self.account = account_name
        self.socket = socket
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.socket)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account:
                    print(f'Получено сообщение от пользователя {message[SENDER]}:\n {message[MESSAGE_TEXT]}')
                elif RESPONCE in message and message[RESPONCE] == 202:
                    print('Получен список контакт листов')
                    contact_list = message[DATA]
                    print(f'Получено {message[RESPONCE]}{message[DATA]} от сервера')
                elif RESPONCE in message and message[RESPONCE] == 500:
                    print('Получено одобрение на добавление в друзья')
                    print(f'Получено {message[RESPONCE]}{message[DATA]}')
                else:
                    print('Получено некорректное сообщение от сервера')
            except:
                break


def create_presence(account_name):
    print('CREATE PRESENCE')
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    print(type(out))
    return out

def login_request_user(account_name, password):
    print('login_request_user func')
    out = {
        ACTION: LOGIN_REQUEST,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD_HASH: password
        }
    }
    return out

def create_register(account_name, password):
    print('Register msg')
    out = {
        ACTION: REGISTER,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
            PASSWORD_HASH: password
        }
    }
    return out


def process_responce_ans(message):
    if RESPONCE in message:
        if message[RESPONCE] == 200:
            return '200: OK'
        elif message[RESPONCE] == 400:
            raise SyntaxError(f'400: {message[ERROR]}')

    print(f'ERROR in PROCESS {message[RESPONCE]}')


def arg_parce():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', default=DEF_IP, nargs='?')
    parser.add_argument('-port', default=DEF_PORT, nargs='?')
    parser.add_argument('-account_name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.ip
    server_port = namespace.port
    client_name = namespace.account_name

    return server_address, server_port, client_name


def main():
    print('Запустил консольного клиента. ')
    server_address, server_port, client_name = arg_parce()
    client_app = QtWidgets.QApplication(sys.argv)


    if not client_name:
        client_name = input('Введите имя пользователя 1: ')



    else:
        print(f'Клиент запущен с ником {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        # Начинать отсюда
        send_msg_finish(transport, create_presence(client_name))
        answer = process_responce_ans(get_message(transport))
        print('Установлено соединение с сервером')
    except:
        print('Error try transport')
    else:

        # client_dialog = MainWindow(transport=transport, client_name=client_name)
        # client_app.exec_()
        # client_dialog = MainWindow(transport, client_name)

        md_reciver = ClientReaderClass(client_name, transport)
        md_reciver.daemon = True
        md_reciver.start()

        md_sender = ClientSenderClass(client_name, transport)
        md_sender.daemon = True
        md_sender.start()

        while True:
            time.sleep(1)
            if md_reciver.is_alive() and md_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    # Dis_test(main)
    main()
