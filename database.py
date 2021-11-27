import json
import sqlite3
database_path = "test.json"

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS test
             (id INTEGER PRIMARY KEY, date text, latitude real, longitude real, amount real)''')

    def insert(self, date, latitude, longitude, amount):
        self.c.execute("INSERT INTO test VALUES (NULL, ?, ?, ?, ?)", (date, latitude, longitude, amount))
        self.conn.commit()

    def fetch(self):
        self.c.execute("SELECT * FROM test")
        rows = self.c.fetchall()
        return rows

    def close(self):
        self.conn.close()