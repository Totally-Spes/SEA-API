import api
from flask import Flask

if __name__ == "__main__":
    app = Flask(__name__)
    API = api.API(app)
    API.run()
