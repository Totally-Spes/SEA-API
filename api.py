import datetime
from datetime import timezone
import location_db
import login
from flask import Flask, request, jsonify

class API:
    def __init__(self, app: Flask):
        self.app = app
        self.app.add_url_rule('/api', 'index', self.__index)
        self.app.add_url_rule('/api/location/get/<latitude>/<longitude>/<radius>', 'getlocation', self.__get_location)
        self.app.add_url_rule('/api/location/get/<latitude>/<longitude>', 'getlocation', self.__get_location)
        self.app.add_url_rule('/api/location/set/<latitude>/<longitude>/<amount>', 'setlocation', self.__set_location)

        # gestion of the login data
        self.app.add_url_rule('/api/login/<username>/<password>', 'login', self.__login)

    def __index(self):
        return 'Hello, World!'

    def __get_location(self, latitude, longitude, radius=10):
        db = location_db.LocationDatabase()
        date = datetime.datetime.now(timezone.utc).timestamp()

        locations = db.fetch_locations(latitude, longitude, radius)

        lat_min = int(latitude) - int(radius)
        lat_max = int(latitude) + int(radius)
        long_min = int(longitude) - int(radius)
        long_max = int(longitude) + int(radius)
        step = 1

        found = False
        cur_lat, cur_long = None, None

        for lat in range (lat_min, lat_max, step):
            for long in range(long_min, long_max, step):
                found = False
                for _, _, cur_lat, cur_long, _ in locations:
                    if lat == cur_lat and long == cur_long:
                        found = True
                        break
                if not found:
                    break
            if not found:
                break

        ret = { cur_lat, cur_long }

        return jsonify(ret)

    def __set_location(self, latitude, longitude, amount):
        db = location_db.LocationDatabase()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, amount)

        return "OK"

    def __login(self, username, password):
        db = login.LoginDatabase()
        return jsonify(db.login(username, password))

    def run(self, port):
        self.app.run(debug=True, port=port)

