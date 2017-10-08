import pymongo, config, feedparser
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
	feed = feedparser.parse(url)
	if len(feed["entries"]) > 0:
		conn.save({
			"_id": url,
		    "source_table": "Article",
			"source_name": feed["feed"]["title"],
			"source_url": url,
			"source_content": "text",
			"source_categories": category.split(",")
		})
		return '{"success": true}'
	return '{"success": false}'

app.run(host='0.0.0.0', port=5001, threaded=True)
