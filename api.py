import datetime
from datetime import timezone
import database
from flask import Flask, request, jsonify


class API:
    def __init__(self,app):
        self.app = Flask(__name__)
        self.app.add_url_rule('/api', 'index', self.__index)  # / -> index
        self.app.add_url_rule('/api/location', 'toto', view_func=self.__get_items_in_region)

    def __index(self):
        return 'Hello, World!'

    def __get_items_in_region(self):
        if 'latitude' in request.args:
            latitude = int(request.args['id'])
        else:
            return 'Error: No id field provided. Please specify an id.'

        if 'longitude' in request.args:
            longitude = int(request.args['longitude'])
        else:
            return 'Error: No longitude field provided. Please specify a longitude.'

        if 'radius' in request.args:
            radius = int(request.args['radius'])
        else:
            radius = 10
            
        db = database.Database()
        date = datetime.datetime.now(timezone.utc).timestamp()
        db.insert(date, latitude, longitude, radius)
        return "OK"
        return 'Seafish '  + str(id)

    def run(self):
        self.app.run(debug=True)


    
