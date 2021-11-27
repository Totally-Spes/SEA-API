from flask import Flask
import datetime
from datetime import timezone
import database

class API:
    def __init__(self, app):
        self.app = app
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/postpath/<latitude>/<longitude>/<amount>', 'route_post_path', self.route_post_path)

    def index(self): 
        return 'Hello, World!'

    def route_post_path(self, latitude, longitude, amount):
        db = database.Database()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, amount)
        return "OK"

    def run(self):
        self.app.run(debug=True)

