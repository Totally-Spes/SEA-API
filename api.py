import datetime
from datetime import timezone
import location_db
import login
import json
from flask import Flask, request, jsonify, make_response

def clear_old(function):
    """
    Clears old entries from the database.
    """
    db = location_db.LocationDatabase()
    db.remove_old_data()

    return function


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

    @clear_old
    def __check_user(self, username):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    @clear_old
    def __check_hash(self, username, hash):
        db = login.LoginDatabase()
        if db.check_user(username):
            if db(username, hash):
                return True
            else:
                return False
        return False
        

    def __edit_user(self, username, hash):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"

        db.edit(username, hash)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    @clear_old
    def __del_user(self, username):
        db = login.LoginDatabase()
        if not db.check_user(username):
            return "User does not exist"
        db.delete(username)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    @clear_old
    def __add_user(self, username, hash):
        db = login.LoginDatabase()
        if db.check_user(username):
            return "User already exists"

        db.insert(username, hash)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    @clear_old
    def __get_box(self):
        db = location_db.LocationDatabase()
        resp = jsonify(db.fetch())
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

    @clear_old
    def __set_box(self, lat1, long1, lat2, long2, amount):
        db = location_db.LocationDatabase()
        date = datetime.datetime.now(timezone.utc).timestamp()
        boxes = db.fetch()
        for i in range(len(boxes)):
            box = boxes[i]
            if str(box[2]) == lat1 and str(box[3]) == long1 and str(box[4]) == lat2 and str(box[5]) == long2: # if the box is already in the database
                if box[1] != date:
                    db.updateAmount(i,box[6] + int(amount),date)
                
                return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

   
        db.insert(date, lat1, long1, lat2, long2, amount)

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    @clear_old
    def __login(self, username, hash):
        db = login.LoginDatabase()
        if db.check_user(username):
            if db.check_hash(username, hash):
                print("Login successful")
                resp = json.dumps({'success':True}), 200, {'ContentType':'application/json',"Access-Control-Allow-Origin": "*"}
            else:
                resp = json.dumps({'success':False}), 300, {'ContentType':'application/json',"Access-Control-Allow-Origin": "*"}
        else:
            resp = json.dumps({'success':False}), 300, {'ContentType':'application/json',"Access-Control-Allow-Origin": "*"}
        return resp
        

    def run(self, port):
        self.app.run(debug=True, port=port)

