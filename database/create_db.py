import sqlite3


def connection(db_name):
    try:
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()

        with open('commands.sql', 'r') as file:
            commands = file.read()

        cursor.executescript(commands)
        print('База данных создана!')
    except ConnectionError as err:
        print(err)
        raise ConnectionError


if __name__ == '__main__':
    connection('database.sqlite')
