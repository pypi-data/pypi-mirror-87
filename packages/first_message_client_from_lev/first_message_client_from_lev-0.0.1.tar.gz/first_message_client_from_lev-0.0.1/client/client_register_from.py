from PyQt5 import QtCore, QtWidgets

from client_class import create_register
from common.external_func import send_msg_finish, get_message
from common.vars import RESPONCE

# Класс фокмы регистрации
class Register_form(QtWidgets.QDialog):
    '''
    Класс фокмы регистрации
    '''

    def __init__(self, transport):
        super().__init__()
        self.ui = Ui_Register_Form()
        self.ui.setupUi(self)
        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.register_button.clicked.connect(self.register_user)
        self.register_flag = None
        self.transport = transport
        self.show()
    # Функция обработки click
    def click(self):
        self.ok_pressed = True
        self.close()
    # Функция отправки запроса регистрации на сервер и распознавание ответа от него
    def register_user(self):
        '''
        Функция отправки запроса регистрации на сервер и распознавание ответа от него
        '''
        if self.ui.login_line_edit and self.ui.password_line_edit:
            password = self.ui.password_line_edit.text().lower()
            print('Password -  ', password)
            username = self.ui.login_line_edit.text().lower()
            print('Username - ', username)
            try:
                send_msg_finish(self.transport, create_register(self.ui.login_line_edit.text().lower(), password))
            except:
                print('Error send message register ')
            answer = get_message(self.transport)
            print(answer)
            if answer[RESPONCE] == 511:
                self.close()
            elif answer[RESPONCE] == 512:
                print('ERROR')
                self.ui.login_line_edit.clear()
                self.ui.password_line_edit.clear()
                # print(answer[ERROR])

        else:
            print('Пустой логин и пароль')

# Форма регистрации
class Ui_Register_Form(object):
    '''
    Форма регистрации
    '''
    def setupUi(self, Register_Form):
        Register_Form.setObjectName("Register_Form")
        Register_Form.resize(400, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Register_Form.sizePolicy().hasHeightForWidth())
        Register_Form.setSizePolicy(sizePolicy)
        Register_Form.setMinimumSize(QtCore.QSize(400, 320))
        Register_Form.setMaximumSize(QtCore.QSize(400, 320))
        self.register_button = QtWidgets.QPushButton(Register_Form)
        self.register_button.setGeometry(QtCore.QRect(60, 220, 112, 32))
        self.register_button.setObjectName("register_button")
        self.cancel_button = QtWidgets.QPushButton(Register_Form)
        self.cancel_button.setGeometry(QtCore.QRect(210, 220, 112, 32))
        self.cancel_button.setObjectName("cancel_button")
        self.login_line_edit = QtWidgets.QLineEdit(Register_Form)
        self.login_line_edit.setGeometry(QtCore.QRect(60, 90, 251, 21))
        self.login_line_edit.setObjectName("login_line_edit")
        self.password_line_edit = QtWidgets.QLineEdit(Register_Form)
        self.password_line_edit.setGeometry(QtCore.QRect(60, 160, 251, 21))
        self.password_line_edit.setObjectName("password_line_edit")
        self.Login_Label = QtWidgets.QLabel(Register_Form)
        self.Login_Label.setGeometry(QtCore.QRect(160, 60, 58, 16))
        self.Login_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Login_Label.setObjectName("Login_Label")
        self.label_2 = QtWidgets.QLabel(Register_Form)
        self.label_2.setGeometry(QtCore.QRect(160, 130, 58, 16))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Register_Form)
        QtCore.QMetaObject.connectSlotsByName(Register_Form)

    def retranslateUi(self, Register_Form):
        _translate = QtCore.QCoreApplication.translate
        Register_Form.setWindowTitle(_translate("Register_Form", "Form"))
        self.register_button.setText(_translate("Register_Form", " Регистрация"))
        self.cancel_button.setText(_translate("Register_Form", "Отмена"))
        self.Login_Label.setText(_translate("Register_Form", "Логин"))
        self.label_2.setText(_translate("Register_Form", "Пароль"))
