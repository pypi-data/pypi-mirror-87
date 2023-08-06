import time
import threading
from PyQt5.QtCore import pyqtSignal, QObject

from common.vars import EXIT, ACTION, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT, \
    RESPONCE, GET_CONTACT, ADD_CONTACT, USER_ID_TO_CONTACT, DATA
from common.external_func import send_msg_finish, get_message

socket_lock = threading.Lock()


# Класс создания сокета для отправки сообщений
class ClientSenderClass(threading.Thread, QObject):
    '''
    Класс создания сокета для отправки сообщений
    '''

    def __init__(self, account_name, socket):
        self.account = account_name
        self.socket = socket
        threading.Thread.__init__(self)
        QObject.__init__(self)

    # Функция создания сообщения о выходе
    def create_exit_message(self):
        '''
            Функция создания сообщения о выходе

        :return: Словарь
        '''
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account
        }

    #  Функция создания сообщения
    def create_message(self, to, message):
        '''
        Функция создания сообщения
        :param to: Кому сообщение
        :param message: само сообщение
        :return: словарь
        '''
        print('Create, message')
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
        except Exception:
            exit(1)

    #  Функция получения списка контактов
    def get_contact(self):
        '''
        Функция получения списка контактов
        :return: Словарь для отправки
        '''
        message_dict = {
            ACTION: GET_CONTACT,
            SENDER: self.account,
            TIME: time.time(),
        }
        print('get_contact')
        return message_dict

    # Функция генерации сообщения для добавления контакта
    def add_contact(self, contact):
        '''
        Функция генерации сообщения для добавления контакта

        :param contact: имя контакта
        :return: возвращает словарь для отправки
        '''
        message_dict = {
            ACTION: ADD_CONTACT,
            SENDER: self.account,
            USER_ID_TO_CONTACT: contact,
            TIME: time.time(),
        }
        return message_dict

    def print_help(self):
        print('------')
        print('message - отправить сообщение. Кому и текст сообщения отдельно')
        print('help - вывести подсказки по командам')
        print('exit - выход ')
        print('list - для получения контактов')
        print('add_contact - для добавления контакта')
        print('------')


# Класс на получение сообщений от сервера
class ClientReaderClass(threading.Thread, QObject):
    '''
    Класс на получение сообщений от сервера
    '''
    new_message = pyqtSignal(list)
    message_from_user = pyqtSignal(dict)

    def __init__(self, account_name, socket):
        self.account = account_name
        self.socket = socket
        # self.contact_list = None
        # super().__init__()
        threading.Thread.__init__(self)
        QObject.__init__(self)

    def run(self):
        '''
        Функция обработки входящих сообщений
        '''
        while True:
            with socket_lock:
                try:
                    message = get_message(self.socket)
                    # print(f'Incoming message {message}')
                    if ACTION in message and message[ACTION] == MESSAGE \
                            and SENDER in message and DESTINATION in message \
                            and MESSAGE_TEXT in message and message[DESTINATION] == self.account:
                        print(f'Получено сообщение от пользователя {message[SENDER]}:\n {message[MESSAGE_TEXT]}')
                        self.message_from_user.emit(message)
                    elif RESPONCE in message and message[RESPONCE] == 202:
                        print('Получен список контакт листов')
                        contact_list = message[DATA]
                        print(f'Получено {message[RESPONCE]}{message[DATA]} от сервера')
                        self.contact_list = contact_list
                        self.new_message.emit(contact_list)
                    elif RESPONCE in message and message[RESPONCE] == 500:
                        print('Получено одобрение на добавление в друзья')
                        print(f'Получено {message[RESPONCE]}{message[DATA]}')
                    else:
                        print('Получено некорректное сообщение от сервера')
                except Exception:
                    print('Socket error')
                    break
