import sys
import time
import socket
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
import argparse
from common.external_func import send_msg_finish
from client_chat_gui_v3 import Ui_MainWindow
from transport import ClientSenderClass, ClientReaderClass
from add_contact_windows import Add_Contact
from chat_dialog import Chat_Dialog
from common.vars import DEF_IP, DEF_PORT
from login_dialog import Login_Dialog_Form


# Класс главного окна.
class MainWindow(QtWidgets.QMainWindow):
    '''
    Класс главного окна.
    '''

    def __init__(self, transport=None, client_name=None, treads=None, parent=None):
        super().__init__()
        self.transport = transport
        self.client_name = client_name
        self.client_sender = treads[1]
        self.client_reciever = treads[0]
        self.client_reciever.new_message.connect(self.get_user_contact_list)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.listWidget.itemDoubleClicked.connect(self.chat_dialog_open)
        self.ui.pushButton_2.clicked.connect(self.add_contact)
        self.send_message()

        self.show()

    #  Открытие чата с пользователем по двойному клику
    def chat_dialog_open(self):
        '''
        Открытие чата с пользователем по двойному клику
        '''
        row = self.ui.listWidget.currentRow()
        print(f'-- row index {row}')
        item = self.ui.listWidget.item(row)
        self.dialog_contact = Chat_Dialog(user_nickname=item.text(), sender=self.client_sender,
                                          reader=self.client_reciever)
        self.dialog_contact.show()

    # Добавление пользователе в список пользователей пришедших с сервера.
    def get_user_contact_list(self, contact_list):
        '''
        Добавление пользователе в список пользователей пришедших с сервера.
        '''
        for i in contact_list:
            self.ui.listWidget.addItem(i)
        print('Generate list rdy')

    #
    def send_message(self):
        self.client_sender.get_contact()
        try:
            send_msg_finish(self.transport, self.client_sender.get_contact())
        except Exception:
            print('Error send msg')

    # Добавить контак в контакт лист
    def add_contact(self):
        '''
        Добавить контак в контакт лист
        '''
        print('-Add contact')
        self.add_contact = Add_Contact()
        self.add_contact.ui.pushButton.clicked.connect(lambda: self.send_contact_to_server(self.add_contact))
        self.add_contact.show()

    # Отправка запроса на получение контакт листа
    def send_contact_to_server(self, item):
        '''
        Отправка запроса на получение контакт листа
        '''
        contact_name = item.ui.textEdit.toPlainText()
        item.ui.textEdit.clear()
        send_msg_finish(self.transport, self.client_sender.add_contact(contact_name))
        self.ui.listWidget.addItem(contact_name)
        print(contact_name)
        print('Send contact to server')

    @pyqtSlot()
    def get_contact_list(self, list):
        print('Get contact')
        print(list)
        print('----')


# Функция создания потоков
def create_client_treads(client_name, transport):
    '''
    Функция создания потоков
    '''
    print('Установлено соединение с сервером')

    print('---- Create_client_treads -----')
    md_reciver = ClientReaderClass(account_name=client_name, socket=transport)
    md_reciver.setDaemon(True)
    md_reciver.start()

    md_sender = ClientSenderClass(account_name=client_name, socket=transport)
    md_sender.setDaemon(True)
    md_sender.start()

    while True:
        time.sleep(1)
        if md_reciver.is_alive() and md_sender.is_alive():
            continue
        break

    return md_reciver, md_sender


# Создание транспортного сокета
def transport_func():
    '''
    Создание транспортного сокета
    '''
    server_address = DEF_IP
    server_port = DEF_PORT

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        print('Установлено соединение с сервером')
    except:
        print('Error try transport')

    return transport


# Парсер аргументов командной строки
def arg_parce():
    '''
    Парсер аргументов командной строки
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', default=DEF_IP, nargs='?')
    parser.add_argument('-port', default=DEF_PORT, nargs='?')
    parser.add_argument('-account_name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.ip
    server_port = namespace.port
    client_name = namespace.account_name

    return server_address, server_port, client_name


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    server_address, server_port, client_name = arg_parce()

    try:
        transport = transport_func()
    except Exception:
        print('Error transport create')
        sys.exit(1)
    else:
        if client_name == None:
            start_dialog = Login_Dialog_Form(transport)
            app.exec_()
            if start_dialog.login_flag == True:
                client_name = start_dialog.ui.lineEdit.text()
                del start_dialog
            else:
                sys.exit(0)

        treads_create = create_client_treads(client_name=client_name, transport=transport)
        progress = MainWindow(transport=transport, client_name=client_name, treads=treads_create)
        progress.show()
        sys.exit(app.exec_())
