# save this as app.py
from flask import Flask, request
from flask_cors import CORS, cross_origin

from crawler import *

app = Flask(__name__)


@app.route('/project', methods=["POST"])
@cross_origin(["http://localhost:3000/"])
def project():
    url = request.json["url"]
    return crawl_project(url)


@app.route('/', methods=["GET"])
def hello():
    return 'Hello'


if __name__ == "__app__":
    # set debug=false in production
    app.run(debug=False)
