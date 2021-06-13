import os
import sqlite3
from os import path
from pathlib import Path
import scripts.globals as global_var

def __init__():
    global base_name
    global c, conn

    base_name = global_var.base_name
    base_exist = path.exists(base_name)

    if not base_exist:
        Path(os.path.dirname(base_name)).mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(base_name, check_same_thread=False)
        c = conn.cursor()
        create_base()
    else:
        print('Base %s exist' % base_name)
        conn = sqlite3.connect(base_name, check_same_thread=False)
        c = conn.cursor()


def create_base():
    global c, conn
    # Create table 
    c.execute('''CREATE TABLE users
                (id INTEGER PRIMARY KEY AUTOINCREMENT,        
                tg_id INTEGER UNIQUE,
                name TEXT,
                last_currency TEXT DEFAULT 'USD'
                )''')

    c.execute('''CREATE TABLE settings
                    (name TEXT UNIQUE,
                    value BLOB
                    )''')

    c.execute('''CREATE TABLE currency
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        code TEXT UNIQUE,
                        nominal REAL,
                        value REAL
                        )''')
    conn.commit()


def insert_data(table, data):
    global c, conn
    val_count = table.count(",")
    val_count = val_count + 1
    if val_count > 1:
        expression = '?,' * val_count
        expression = expression[:-1]
    else:
        expression = '?'
    expression = '(' + expression + ')'
    sql = 'INSERT INTO {table} VALUES {ex}'
    sql = sql.format(table=table, ex=expression)
    c.executemany(sql, data)
    conn.commit()


def replace_data(table, data):
    global c, conn
    val_count = table.count(",")
    val_count = val_count + 1
    if val_count > 1:
        expression = '?,' * val_count
        expression = expression[:-1]
    else:
        expression = '?'
    expression = '(' + expression + ')'
    sql = 'REPLACE INTO {table} VALUES {ex}'
    sql = sql.format(table=table, ex=expression)
    c.executemany(sql, data)
    conn.commit()


def update_data(table, expression, data):
    global c, conn
    sql = 'UPDATE {table} {ex}'
    sql = sql.format(table=table, ex=expression)
    c.executemany(sql, data)
    conn.commit()


def select(what, table, expression=''):
    global c, conn

    if expression != '':
        sql = 'SELECT {what} FROM {table} WHERE {ex}'
        sql = sql.format(what=what, table=table, ex=expression)
    else:
        sql = 'SELECT {what} FROM {table}'
        sql = sql.format(what=what, table=table)

    c.execute(sql)
    data_str = c.fetchall()
    return data_str


def select_adw(what, table, expression):
    global c, conn
    sql = 'SELECT {what} FROM {table} {ex}'
    sql = sql.format(what=what, table=table, ex=expression)
    c.execute(sql)
    data_str = c.fetchall()
    return data_str


def command_adw(what):
    global c, conn
    c.execute(what)
    conn.commit()

global_var.init()
__init__()
