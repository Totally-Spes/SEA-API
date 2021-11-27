import datetime
from datetime import timezone
import database
from flask import Flask, request, jsonify

class API:
    def __init__(self, app: Flask):
        self.app = app
        self.app.add_url_rule('/api', 'index', self.__index)
        self.app.add_url_rule('/api/location/get/<latitude>/<longitude>/<radius>', 'getlocation', self.__get_location)
        self.app.add_url_rule('/api/location/set/<latitude>/<longitude>/<amount>', 'setlocation', self.__set_location)

    def __index(self):
        return 'Hello, World!'

    def __get_location(self, latitude, longitude, radius):
        db = database.Database()
        date = datetime.datetime.now(timezone.utc).timestamp()
        return jsonify(db.get_location(date, latitude, longitude, radius))

        # locations = db.get_locations(date, latitude, longitude, radius)

        return jsonify(locations)

    def __set_location(self, latitude, longitude, amount):
        db = database.Database()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, amount)

        return "OK"

    def run(self):
        self.app.run(debug=True)

