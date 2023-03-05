import sqlite3

conn = sqlite3.connect("Artistc.db")
cursor = conn.cursor()

# Вопрос 1. Информация о скольких художниках представлена в базе данных?
cursor.execute('SELECT * FROM artists')
data = cursor.fetchall()
print('Количество художников в базе:', len(data))

# Вопрос 2. Сколько женщин (Female) в базе?
cursor.execute('SELECT * FROM artists WHERE gender == "Female"')
data = cursor.fetchall()
print('Количество женщин:', len(data))

# Вопрос 3. Сколько человек в базе данных родились до 1900 года?
cursor.execute('SELECT * FROM artists WHERE "Birth Year" < 1900')
data = cursor.fetchall()
print('Родились до 1900 года:', len(data))

# Вопрос 4*. Как зовут самого пожилого художника?

# Вариант решения 1: используем стандартные средства Python
cursor.execute('SELECT * FROM artists WHERE "Birth Year" < 1900')
data = cursor.fetchall()
oldest = {'name': '', 'birthday': 1900}
for person in data:
    if person[4] < oldest['birthday']:
        oldest['name'] = person[1]
        oldest['birthday'] = person[4]
print('Самый старший:', oldest)

# Вариант решения 2: только SQL
cursor.execute('SELECT name FROM artists WHERE "Birth Year" < 1900 order by "Birth Year"')
data = cursor.fetchall()
print('Самый старший:', data[0][0])

conn.commit()
