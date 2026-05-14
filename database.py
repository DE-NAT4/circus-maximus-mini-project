import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS couriers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT
            )
            '''
        )
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS product_menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                price REAL
            )
            '''
        )
        conn.commit()


def fetch_all(table_name, order_by='id'):
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(f'SELECT * FROM {table_name} ORDER BY {order_by}')
        return [dict(row) for row in cursor.fetchall()]


def execute(query, params=None, commit=False):
    init_db()
    params = params or ()
    with get_connection() as conn:
        cursor = conn.execute(query, params)
        if commit:
            conn.commit()
        return cursor
