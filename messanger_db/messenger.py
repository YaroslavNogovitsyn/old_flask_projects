import time

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from messanger_db.ui_froms import clientui, new_enter, new_registration, code_input, code_view, del_messages


def show_error(text):
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Ошибка!")
    msgBox.setText(text)
    msgBox.exec_()


class Enter(QtWidgets.QWidget, new_enter.Ui_Enter):
    def __init__(self):
        super().__init__()
        # Подключение настроек
        self.setupUi(self)
        # Подключение кнопки входа
        self.enter_btn.clicked.connect(self.send_enter)
        # Подключение кнопки перехода на регистрацию
        self.enter_registration_btn.clicked.connect(self.start_registration)
        self.window = ''

    def send_enter(self):
        username = self.enter_login.text()
        password = self.enter_password.text()
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://127.0.0.1:5000/enter', json=data)
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
            return
        if response.status_code == 400:
            self.enter_password.setText('Error')
            self.enter_login.setText('Error')
        elif response.status_code == 401:
            self.enter_password.setText('Вы не зарегистрированы')
            self.enter_login.setText('Вы не зарегистрированы')
        else:
            self.close()
            self.window = MainWindow()
            self.window.show()


    def start_registration(self):
        self.close()
        self.start = Registration()
        self.start.show()


class Registration(QtWidgets.QWidget, new_registration.Ui_Registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.registration_btn.clicked.connect(self.send_registration)

    def send_registration(self):
        name = self.registration_name.text()
        username = self.registration_login.text()
        password = self.registration_password.text()
        data = {'name': name, 'username': username, 'password': password}
        try:
            response = requests.post('http://127.0.0.1:5000/registration', json=data)
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
            return
        if response.status_code == 401:
            error = QtWidgets.QMessageBox()
            error.setText('Такой логин уже существует')
            error.setWindowTitle('Ошибка')
            error.exec_()
        else:
            self.close()
            self.start = Enter()
            self.start.show()


# Создание поля для редактирования онлайн-кода
class CodeInput(QtWidgets.QMainWindow, code_input.Ui_MainWindow):
    # Определение базового класса
    def __init__(self):
        super().__init__()
        # Подключение настроек
        self.setupUi(self)
        try:
            data = requests.get('http://127.0.0.1:5000/enter').json()
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
        # Добавление имени, забранного с поля регистрации
        self.name_code.setText(data['name'][0])
        # Подключение кнопки сохранения кода
        # self.save_btn.clicked.connect(self.send_message_code)
        self.exit_btn.clicked.connect(self.exit_from)
        # Определение встроенного таймера отправки сообщения
        self.timer = QtCore.QTimer()
        # Определение разницы между GET и POST запросами на сервер
        self.timer.start(1000)
        # Определение параметра сортировки сообщений по времени
        self.after = 0
        while True:
            self.send_message_code()
            time.sleep(3)

    # Функция отправки сообщений на сервер
    def send_message_code(self):
        # Забираем данные из поля, где прописано имя
        name = self.name_code.text()
        # Забираем данные из поля ввода кода
        text = self.code_input.toPlainText()
        # Преобразование в словарь для использования формата json
        data = {'name': name, 'text': text}
        try:
            response = requests.post('http://127.0.0.1:5000/codesendinput', json=data)
        except:
            self.code_input.append('Сервер недоступен\n')
            show_error("Сервер недоступен. Попробуйте позже.")
            return
        # Если ответ от сервера отрицательный, то окно закрывается
        if response.status_code != 200:
            self.close()

    def exit_from(self):
        self.close()
        self.window = MainWindow()
        self.window.show()


# Создание поля стрима
class CodeView(QtWidgets.QMainWindow, code_view.Ui_MainWindow):
    # Определение базового класса
    def __init__(self):
        super().__init__()
        # Подключение настроек
        self.setupUi(self)
        # Определение встроенного таймера отправки сообщения
        self.timer = QtCore.QTimer()
        # Подключение таймера к функции отправки сообщений
        self.timer.timeout.connect(self.load_messages_code_view)
        # Определение разницы между GET и POST запросами на сервер
        self.timer.start(1000)
        # Определение параметра сортировки сообщений по времени
        self.after = 0

        try:
            data = requests.get('http://127.0.0.1:5000/enter').json()
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
        # Добавление имени, забранного с поля регистрации
        self.code_writer.setText(data['name'][0])

    # Подключение функции для преобразования json формата в текстовой вид
    def pretty_messages_code_view(self, message):
        self.code_view.append(message['text'])
        self.code_view.append('')
        print(time.strftime("%H:%M:%S", time.localtime(message['time'])))

    # Подключаем функцию загрузки сообщений в поле просмотра стрима
    def load_messages_code_view(self):
        try:
            data = requests.get('http://127.0.0.1:5000/codemessage', params={'after': self.after}).json()
        except:
            return
        print(data['messagescode'])
        # Вывод сообщений в поле просмотра стрима на основе параметра json
        for message in data['messagescode']:
            self.pretty_messages_code_view(message)
            self.after = message['time']


# Создание основного окна мессенджера
class MainWindow(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    # Определение базового класса
    def __init__(self):
        super().__init__()
        # Подключение настроек
        self.setupUi(self)
        # Подключение кнопки отправки сообщений
        self.btn_send.clicked.connect(self.send_message)
        # Подключение кнопки перехода на окно редактирования кода
        self.btn_code.clicked.connect(self.start_online_code_input)
        # Подключение кнопки перехода на окно просмотра стрима
        self.btn_code_strim.clicked.connect(self.start_online_code_strim)
        # Подключение кнопки удаления сообщений
        self.btn_del.clicked.connect(self.delete_messages)

        # Определение встроенного таймера отпрвки сообщения
        self.timer = QtCore.QTimer()
        # Подключение таймера к функции отправки сообщений
        self.timer.timeout.connect(self.load_messages)
        # Определение разницы между GET и POST запросами на сервер
        self.timer.start(5000)
        # Определение параметра сортировки сообщений по времени
        self.after = 0
        try:
            data = requests.get('http://127.0.0.1:5000/enter').json()
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
        # Добавление имени, забранного с поля регистрации
        self.name.setText(data['name'][0])
        self.load_messages()

    def pretty_messages_all(self, message):
        self.messages.append(
            message['name'] + ' ' + time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime(message['time'])))
        self.messages.append(message['text'])
        self.messages.append('')

    # Функция отправки сообщений на сервер

    def send_message(self):
        # Забираем данные из поля, где прописано имя
        name = self.name.text()
        # Забираем данные из поля ввода кода
        text = self.text.toPlainText()
        # Преобразование в словарь для использования формата json
        data = {'name': name, 'text': text}
        try:
            response = requests.post('http://127.0.0.1:5000/send', json=data)
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
            return
        # Если ответ сервера не положительный:
        if response.status_code != 200:
            if not name:
                self.name.setText('Введите имя!')
                return
        # Сброс значений поля отправки сообщений
        self.text.setText('')
        self.load_messages()

    # Подключение функции для преобразования json формата в текстовой вид
    def pretty_messages(self, message):
        self.messages.append(
            message['name'] + ' ' + time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime(message['time'])))
        self.messages.append(message['text'])
        self.messages.append('')
        print(time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime(message['time'])))
        print(message['time'])

    # Подключаем функцию загрузки сообщений в поле просмотра сообщений
    def load_messages(self):
        try:
            data = requests.get('http://127.0.0.1:5000/messages', params={'after': self.after}).json()
        except:
            show_error("Сервер недоступен. Попробуйте позже.")
            return
        # Вывод сообщений в поле просмотра сообщений на основе параметра json
        for message in data['messages']:
            self.pretty_messages(message)
            self.after = message['time']

    # Функция запуска поля для редактирования кода
    def start_online_code_input(self):
        self.close()
        self.online = CodeInput()
        self.online.show()

    # Функция запуска поля для просмотра стрима
    def start_online_code_strim(self):
        self.close()
        self.online_strim = CodeView()
        self.online_strim.show()

    # Функция запуска окна удаления сообщений
    def delete_messages(self):
        if self.btn_del.text() == 'Delete':
            self.delete = DeleteMessages()
            self.delete.show()
            self.btn_del.setText('Обновить')
        else:
            try:
                new_data = requests.get('http://127.0.0.1:5000/rewrite').json()
            except:
                show_error("Сервер недоступен. Попробуйте позже.")
                return
            for message in new_data['rewrited_messages']:
                self.pretty_messages(message)
            self.btn_del.setText('Delete')


# Создание окна удаления сообщений
class DeleteMessages(QtWidgets.QDialog, del_messages.Ui_del_messages):
    # Определение базового класса
    def __init__(self):
        # Подключение настроек
        super().__init__()
        # Подключение настроек
        self.setupUi(self)
        # Подключение кнопки отправки времени
        self.delButton.clicked.connect(self.delete_messages_main)

    def delete_messages_main(self):
        # Забираем значения часа
        hours = self.hours.text()
        # Забираем значение минут
        minutes = self.minutes.text()
        # Забираем значение секунд
        seconds = self.seconds.text()
        # Преобразование в словарь для использования формата json
        full_date = {'hours': hours, 'minutes': minutes, 'seconds': seconds}
        try:
            response = requests.post('http://127.0.0.1:5000/delmessage', json=full_date)
        except:
            return self.close()

        # Если ответ сервера положительный, то
        if response.status_code == 200:
            self.choose_time.setText('Сообщение удалено')
        # Если в списке сообщений нет такого сообщения, то
        if response.status_code == 400:
            self.choose_time.setText('Такого сообщения нет')
        # Если не были введены все данные
        if response.status_code == 405:
            self.choose_time.setText('Вы не ввели данные')


# Запуск окна входа
dialog = QtWidgets.QApplication([])
d = Enter()
d.show()
dialog.exec_()
