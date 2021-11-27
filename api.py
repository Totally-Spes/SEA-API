import datetime
from datetime import timezone
import location_db
import login
import json
from flask import Flask, request, jsonify, make_response

class API:
    def __init__(self, app: Flask):
        self.app = app
        self.app.add_url_rule('/', 'root', self.__index)
        self.app.add_url_rule('/api', 'index', self.__index)
        self.app.add_url_rule('/api/location/get/<latitude>/<longitude>/<radius>', 'getlocation', self.__get_location)
        self.app.add_url_rule('/api/location/get/<latitude>/<longitude>', 'getlocation', self.__get_location)
        self.app.add_url_rule('/api/location/set/<latitude>/<longitude>/<amount>', 'setlocation', self.__set_location)

        # gestion of the login data
        self.app.add_url_rule('/api/account/login/<username>/<hash>', 'login', self.__login)
        self.app.add_url_rule('/api/account/add/<username>/<hash>', 'add-user', self.__add_user)
        self.app.add_url_rule('/api/account/del/<username>', 'del-user', self.__del_user)
        self.app.add_url_rule('/api/account/edit/<username>/<hash>', 'edit-user', self.__edit_user)

    def __index(self):
        return 'Hello, World!'
    def __check_user(self, username):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        
    
    def __edit_user(self, username, hash):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"

        db.edit(username, hash)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    def __del_user(self, username):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"
        db.delete(username)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    def __add_user(self, username, hash):
        db = login.LoginDatabase()
        if db.check_user(username):
            return "User already exists"

        db.insert(username, hash)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

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

        L = []

        for lat in range (lat_min, lat_max, step):
            for long in range(long_min, long_max, step):
                found = False
                for _, _, cur_lat, cur_long, _ in locations:
                    if lat == cur_lat and long == cur_long:
                        found = True
                        break
                if not found:
                    L.append((lat, long))

        return jsonify(L)

    def __set_location(self, latitude, longitude, amount):
        db = location_db.LocationDatabase()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, amount)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    def __login(self, username, hash):
        db = login.LoginDatabase()
        return jsonify(db.login(username, hash))

    def run(self, port):
        self.app.run(debug=True, port=port)

