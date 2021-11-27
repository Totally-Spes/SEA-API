#! /usr/bin/env python3

from flask import request
import datetime
from datetime import timezone
import database

from flask import Flask

app = Flask(__name__)

@app.route("/")
def root_main():
    return "Hello, World!"

@app.route("/test1/<test>")
def root_test1(test):
    return "hello " + test


@app.route("/test2")
def root_test2():
    return "hello " + request.args.get("name")

@app.route("/postpath/<latitude>/<longitude>/<amount>")
def route_post_path(latitude, longitude, amount):
    db = database.Database()
    date = datetime.datetime.now(timezone.utc).timestamp()
    db.insert(date, latitude, longitude, amount)
    return "OK"