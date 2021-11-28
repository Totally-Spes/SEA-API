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

    def edit(self, email, hash):
        self.c.execute("UPDATE test SET hash=? WHERE email=?", (hash, email))
        self.conn.commit()


    def close(self):
        self.conn.close()

    def login(self, email, hash):
        self.c.execute("SELECT * FROM test WHERE email=? AND hash=?", (email, hash))
        rows = self.c.fetchall()
        if rows:
            return True
        else:
            return False

    def check_user(self, email):
        self.c.execute("SELECT * FROM test WHERE email=?", (email,))
        rows = self.c.fetchall()
        if rows:
            return True
        else:
            return False
        
        
    def check_hash(self, email, hash):
        self.c.execute("SELECT * FROM test WHERE email=?", (email,))
        rows = self.c.fetchall()
        return False if not rows else rows[0][3] == hash
    
    def get_user_id(self, email):
        self.c.execute("SELECT * FROM test WHERE email=?", (email,))
        rows = self.c.fetchall()
        if len(rows) > 0: 
            return rows[0][1]
        else: 
            return None