import api
from flask import Flask

app = Flask(__name__)

API = api.API(app)
API.run()