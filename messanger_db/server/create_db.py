import sqlite3

db_name = 'messenger.sqlite'


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def do(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def create(self):
        self.cursor.execute('PRAGMA foreign_key=on')
        self.do('''CREATE TABLE IF NOT EXISTS users(
                                                id INTEGER PRIMARY KEY,
                                                name VARCHAR,
                                                username VARCHAR,
                                                password VARCHAR)''')
        self.do('''CREATE TABLE IF NOT EXISTS messeges(
                                                    id INTEGER PRIMARY KEY,
                                                    time VARCHAR,
                                                    text VARCHAR,
                                                    user_id INTEGER)''')
        

    def get_name_to_main_window(self, username_global):
        self.cursor.execute('SELECT name FROM users WHERE username=?', [username_global])
        result_name = self.cursor.fetchone()
        
        return result_name

    def check_users(self, username):
        self.cursor.execute('SELECT username from users WHERE username=?', [username])
        result = self.cursor.fetchone()
        
        return result

    def insert_users(self, name, username, password):
        self.cursor.execute('INSERT INTO users(name, username, password) VALUES(?,?,?)', [name, username, password])
        self.conn.commit()
        

    def input_user(self, username_input, password_input):
        self.cursor.execute('SELECT username, password FROM users WHERE username=? AND password=?',
                            [username_input, password_input])
        result = self.cursor.fetchone()
        
        return result

    def send_all_messages(self):
        self.cursor.execute('''SELECT users.name, messeges.time, messeges.text
    FROM users, messeges 
    WHERE users.id=messeges.user_id
    ORDER BY messeges.id''')
        all_messages = self.cursor.fetchall()
        
        return all_messages

    def get_username_to_send_message(self, username_global):
        self.cursor.execute('''SELECT id FROM users WHERE username=?''', [username_global])
        id_of_user = self.cursor.fetchone()
        return id_of_user

    def send_one_message(self, time_of_message, message, username_global):
        #     self.cursor.execute('''INSERT INTO messeges (time, text, user_id)
        # VALUES (?, ?, SELECT * from (select id from users where username=?) as query
        #  ''')
        information = self.get_username_to_send_message(username_global)
        self.cursor.execute('INSERT INTO messeges(time, text, user_id) VALUES(?,?,?)',
                            [time_of_message, message, information[0]])
        self.conn.commit()
        

    def delete(self):
        query = """DROP TABLE IF EXISTS users"""
        self.do(query)
        new_query = '''DROP TABLE IF EXISTS messages'''
        self.do(new_query)
        
