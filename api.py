from flask import Flask

class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', 'index', self.index) # / -> index
        self.app.add_url_rule('/<path:path>', 'index', self.seafish) # /<path:path> -> index

    def index(self): 
        return 'Hello, World!'

    def seafish(self):
        return 'Seafish'

    def run(self):
        self.app.run(debug=True)


    
