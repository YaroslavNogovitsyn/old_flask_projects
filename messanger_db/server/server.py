import time
from flask import Flask, request, Response
from create_db import DataBase

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'VERY_STRONG_CODE'
messages = [  # {'name': 'Vasya', 'text': 'Привет', 'time': time.time()},
    # {'name': 'Petya', 'text': 'Пока', 'time': time.time()}
]
code_messages = [

]

database = DataBase()
username_global = ''


# Создаём функцию по фильтрации сообщений для основного окна мессенджера по времени отправки
def filter_by_key(elements, key, thresold):
    filtered_elements = []
    for elem in elements:
        if elem[key] > thresold:
            filtered_elements.append(elem)
    return filtered_elements


# Создаём функцию по фильтрации сообщений для окна кода по времени отправки
def filter_by_key_code(elements, key, thresold):
    filtered_elements = []
    for elem in elements:
        if elem[key] > thresold:
            filtered_elements.append(elem)
    return filtered_elements


def get_all_messages():
    all = database.send_all_messages()
    for elem in all:
        message = {'name': elem[0], 'text': elem[2], 'time': float(elem[1])}
        messages.append(message)
    print(messages)


get_all_messages()


# Запуск сервера - основная страница
@app.route("/")
def hello():
    return "Working... <a href='/status'>Статус</a>"


# Осуществление регистрации в мессенджере
@app.route("/enter", methods=['GET', 'POST'])
def enter_users():
    global username_global
    # Если идёт отпрвка данных на данную страницу
    if request.method == 'POST':
        username_global = request.json['username']
        print(username_global)
        username = request.json['username']
        print(username)
        password = request.json['password']
        full_enter = {'username': username, 'password': password}
        if full_enter['username'] == '' or full_enter['password'] == '':
            return Response(status=400)
        else:
            res = database.input_user(username, password)
            print(res)
            if not res:
                return Response(status=401)
            else:
                if res[0] == username and res[1] == password:
                    return Response(status=200)
                else:
                    return Response(status=401)
    # Если надо получить данные со страницы
    if request.method == 'GET':
        print(username_global)
        result = database.get_name_to_main_window(username_global)
        print(result)
        return {'name': result}
        # Возвращает данные в виде словаря, чтобы можно было использовать json
        # return {'name': f'{user_name} {user_surname}'}


@app.route("/registration", methods=['POST'])
def reg_users():
    if request.method == 'POST':
        new_name = request.json['name']
        new_username = request.json['username']
        new_password = request.json['password']
        all_information = {'new_name': new_name, 'new_username': new_username, 'new_password': new_password}
        if all_information['new_name'] == '' or all_information['new_username'] == '' or all_information['new_password'] == '':
            return Response(status=400)
        else:
            if not database.check_users(all_information['new_username']):
                database.insert_users(new_name, new_username, new_password)
                return Response(status=200)
            else:
                return Response(status=401)


@app.route('/send_all')
def send_all():
    return {'all_messages': messages}


# Работа с обработкой данных на сервер, отправленных с основного окна мессенджера(Связано с функцией send_message)
@app.route("/send", methods=['POST'])
def send():
    # Запрос данных в json формате из messenger.py
    name = request.json['name']
    text = request.json['text']
    message = {'name': name, 'text': text, 'time': time.time()}
    message['name'] = message['name'].strip()
    message['text'] = message['text'].strip()
    message['text'] = message['text'].replace('\n', '')
    # Обработка принятых данных
    if message['name'] == '':
        return Response(status=400)
    else:
        if message['text'] == '':
            return Response(status=400)
        else:
            print(message)
            # В общий список словарей messages записывается сообщение
            database.send_one_message(str(message['time']), message['text'], username_global)
            print(username_global)
            messages.append(message)
            print(messages)
            return Response(status=200)


# Работа с обработкой данных, которые лежат в списке словарей messages(Связано с функцией load_messages)
@app.route("/messages")
def messages_view():
    # Параметр after нужен для правильной сортировки сообщений
    after = float(request.args['after'])
    filtered_messages = filter_by_key(messages, 'time', after)
    # Возвращает данные в виде словаря, чтобы можно было использовать json
    return {'messages': filtered_messages}


# Работа с обработкой данных на сервер, отправленных с окна кода(Связано с функцией send_message)
@app.route("/codesendinput", methods=['POST'])
def send_code_input():
    # Запрос данных в json формате из messenger.py
    name = request.json['name']
    text = request.json['text']
    message_of_code = {'name': name, 'text': text, 'time': time.time()}
    message_of_code['name'] = message_of_code['name'].strip()
    message_of_code['text'] = message_of_code['text'].strip()
    # Обработка принятых данных
    if message_of_code['name'] == '':
        return Response(status=400)
    else:
        print(message_of_code)
        # В общий список словарей messages записывается сообщение
        code_messages.append(message_of_code)
        print(code_messages)
        return Response(status=200)


# Работа с обработкой данных, которые лежат в списке словарей code_messages
@app.route("/codemessage")
def messages_view_code():
    # Параметр after нужен для правильной сортировки сообщений
    after = float(request.args['after'])
    filtered_messages = filter_by_key_code(code_messages, 'time', after)
    # Возвращает данные в виде словаря, чтобы можно было использовать json
    return {'messagescode': filtered_messages}


# Работа с удалением сообщений
@app.route("/delmessage", methods=['POST'])
def del_messages():
    # Забираем отправленные данные
    hours = request.json['hours']
    minutes = request.json['minutes']
    seconds = request.json['seconds']
    full_date_server = {'hours': hours, 'minutes': minutes, 'seconds': seconds}
    # Если введены не все данные, то
    if full_date_server['hours'] == '' or full_date_server['minutes'] == '' or full_date_server['seconds'] == '':
        return Response(status=405)
    else:
        count = 0
        for i in range(len(messages)):
            # Превращаем время в читаемый формат
            time_format = time.strftime("%H:%M:%S", time.localtime(messages[i]['time']))
            # Сравниваем полученные данные и срезы из time_format
            if full_date_server['hours'] == time_format[0:2] and full_date_server['minutes'] == time_format[3:5] \
                    and full_date_server['seconds'] == time_format[6:]:
                # Удаляемый совпавшее сообщение
                messages.pop(i)
                return Response(status=200)
            else:
                count += 1
                if count == len(messages):
                    return Response(status=400)


app.run(port=5000)
