from PyQt5 import QtCore, QtWidgets

from client_class import login_request_user
from client_register_from import Register_form
from common.external_func import send_msg_finish, get_message
from common.vars import RESPONCE


# Класс диалогового окна Login
class Login_Dialog_Form(QtWidgets.QDialog):
    '''
    Класс диалогового окна Login

    '''

    def __init__(self, transport):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ok_pressed = False
        self.transport = transport
        self.ui.pushButton.clicked.connect(self.logint_request)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.register_form_load.clicked.connect(self.go_to_register_window)
        self.login_flag = False
        self.show()

    # Функция обработки
    def click(self):
        self.ok_pressed = True
        self.close()

    # Функция обработки открытия ока регистрации
    def go_to_register_window(self):
        '''
        Функция обработки открытия ока регистрации
        '''
        self.add_contact = Register_form(self.transport)
        self.add_contact.show()

    #  Функция отправк  на сервер запроса на login и его обработка
    def logint_request(self):
        '''
        Функция отправк  на сервер запроса на login и его обработка
        '''
        if self.ui.lineEdit.text() and self.ui.password_line_edit_login.text():
            account_user = self.ui.lineEdit.text()
            password = self.ui.password_line_edit_login.text()

            try:
                send_msg_finish(self.transport, login_request_user(account_name=account_user,
                                                                   password=password))
            except Exception:
                print('Error send_msg_finis | login_request')
            else:
                answer = get_message(self.transport)
                print(answer)
                if answer[RESPONCE] == 515:
                    print('Login ok')
                    self.login_flag = True
                    self.close()

                elif answer[RESPONCE] == 516:
                    self.login_flag = False
                    print('Ошибка поля логин - пароль')


# Форма логина
class Ui_Form(object):
    '''
    Форма логина
    '''
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 220)
        Form.setMinimumSize(QtCore.QSize(400, 220))
        Form.setMaximumSize(QtCore.QSize(400, 220))
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 120, 112, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 120, 112, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(62, 40, 251, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(70, 20, 241, 16))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.password_line_edit_login = QtWidgets.QLineEdit(Form)
        self.password_line_edit_login.setGeometry(QtCore.QRect(60, 90, 251, 21))
        self.password_line_edit_login.setObjectName("password_line_edit_login")
        self.password_label = QtWidgets.QLabel(Form)
        self.password_label.setGeometry(QtCore.QRect(150, 70, 58, 16))
        self.password_label.setAlignment(QtCore.Qt.AlignCenter)
        self.password_label.setObjectName("password_label")
        self.register_form_load = QtWidgets.QPushButton(Form)
        self.register_form_load.setGeometry(QtCore.QRect(140, 170, 112, 32))
        self.register_form_load.setObjectName("register_form_load")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", " Войти"))
        self.pushButton_2.setText(_translate("Form", "Закрыть"))
        self.label.setText(_translate("Form", "Введите никнейм"))
        self.password_label.setText(_translate("Form", " Пароль"))
        self.register_form_load.setText(_translate("Form", "Регистрация"))
