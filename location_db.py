import json
import sqlite3

class LocationDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('location.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS test
             (id INTEGER PRIMARY KEY, date text, lat1 real, long1 real, lat2 real, long2 real, amount real)''')

    def insert(self, date, lat1, long1, lat2, long2, amount):
        self.c.execute("INSERT INTO test VALUES (NULL, ?, ?, ?, ?, ?, ?)", (date, lat1, long1, lat2, long2, amount))
        self.conn.commit()

    def fetch(self):
        self.c.execute("SELECT * FROM test")
        rows = self.c.fetchall()
        return rows

    def fetch_locations(self, latitude, longitude, radius):
        lat_min = int(latitude) - int(radius)
        lat_max = int(latitude) + int(radius)
        long_min = int(longitude) - int(radius)
        long_max = int(longitude) + int(radius)
        cond = 'latitude >= ' + str(lat_min) + ' AND latitude <= ' + str(lat_max) + \
        ' AND longitude >= ' + str(long_min) + ' AND longitude <= ' + str(long_max)
        print(cond)
        self.c.execute('SELECT * FROM test WHERE (' + cond + ')')
        rows = self.c.fetchall()
        return rows

    async def remove_old_data(self):
        # get all data from database which has been stored for more than 20 day
        self.c.execute("SELECT * FROM test WHERE date < date('now', '-20 day')")
        rows = self.c.fetchall()
        for row in rows:
            self.c.execute("DELETE FROM test WHERE id = ?", (row[0],))
        self.conn.commit()


    def close(self):
        self.conn.close()