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
        self.app.add_url_rule('/api/location/setbox/<lat1>/<long1>/<lat2>/<long2>/<amount>', 'setbox', self.__set_box)
        self.app.add_url_rule('/api/location/getbox', 'getbox', self.__get_box)

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

    def __get_box(self):
        db = location_db.LocationDatabase()
        return jsonify(db.fetch())

    def __set_box(self, lat1, long1, lat2, long2, amount):
        db = location_db.LocationDatabase()
        boxes = db.fetch()
        for box in boxes:
            if str(box[2]) == lat1 and str(box[3]) == long1 and str(box[4]) == lat2 and str(box[5]) == long2:
                return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, lat1, long1, lat2, long2, amount)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    def __login(self, username, hash):
        db = login.LoginDatabase()
        return jsonify(db.login(username, hash))

    def run(self, port):
        self.app.run(debug=True, port=port)

