import pymongo, config
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
conn = pymongo.MongoClient()[config.mongo_db][config.mongo_col]

@app.route("/")
def index():
    url = request.args.get("url") if request.args.get("url") else ""
    category = request.args.get("category") if request.args.get("category") else ""
    return store(url, category)

def store(url, category):
	return "OK"

app.run(host='0.0.0.0', port=6000, threaded=True)
