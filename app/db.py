import sqlite3
import app.user_data
import threading

lock = threading.Lock()


def init():
    connect = sqlite3.connect("users.db")
    cursor = connect.cursor()

    s = list()
    for section, subsections in app.user_data.datas.items():
        for rus, eng in subsections.items():
            s.append(eng + ' TEXT')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            nickname TEXT PRIMARY KEY,
            {}
        )
    '''.format(',\n'.join(s)))

    connect.commit()
    connect.close()


def get(nickname, keys):
    with lock:
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()

        print('''
            SELECT {} FROM users WHERE nickname = "{}"
        '''.format(', '.join(keys), nickname))

        cursor.execute('''
            SELECT {} FROM users WHERE nickname = "{}"
        '''.format(', '.join(keys), nickname))

        result = cursor.fetchone()

        connect.close()

        return result


def update(nickname, data):
    with lock:
        connect = sqlite3.connect("users.db")
        cursor = connect.cursor()

        keys = list()
        for rus, eng in app.user_data.simple.items():
            keys.append(eng)

        cursor.execute('''
            SELECT {} FROM users WHERE nickname = "{}"
        '''.format(', '.join(keys), nickname))

        result = list(cursor.fetchone())

        for k, v in data.items():
            i = keys.index(k)
            result[i] = v

        cursor.execute('''
            INSERT OR REPLACE INTO users (nickname, {})
            VALUES ({})
        '''.format(', '.join(keys), '"' + nickname + '", ' + ', '.join('"' + ('' if i is None else i) + '"' for i in result)))

        connect.commit()
        connect.close()
