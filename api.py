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

        return jsonify(locations)

    def __set_location(self, latitude, longitude, amount):
        db = location_db.LocationDatabase()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, amount)

        return "OK"

    def __login(self, username, password):
        db = login.LoginDatabase()
        return jsonify(db.login(username, password))

    def run(self):
        self.app.run(debug=True)

