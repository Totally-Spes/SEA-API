import json
import sqlite3
import hashlib
import uuid

class LoginDatabase():
    def __init__(self):
        self.conn = sqlite3.connect('login.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS test
             (id INTEGER PRIMARY KEY,uuid text, email text, hash text)''')

    def insert(self, email, hash):
        # generate a random uuid
        uuid_id = str(uuid.uuid4())
        # get the hash of the password
        self.c.execute("INSERT INTO test (uuid, email, hash) VALUES (?, ?, ?)", (uuid_id, email, hash))
        self.conn.commit()

    def delete(self, id):
        self.c.execute("DELETE FROM test WHERE id=?", (id,))
        self.conn.commit()

    def fetch(self):
        self.c.execute("SELECT * FROM test")
        rows = self.c.fetchall()
        return rows

    def close(self):
        self.conn.close()

    def login(self, email, password):
        # get the hash of the password
        hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.c.execute("SELECT * FROM test WHERE email=? AND hash=?", (email, hash))
        rows = self.c.fetchall()
        if rows:
            return True
        else:
            return False