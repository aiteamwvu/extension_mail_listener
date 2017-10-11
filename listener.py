import pymongo, config, feedparser
from flask import Flask, request
from flask_cors import CORS
from get_info import *
app = Flask(__name__)
CORS(app)
conn = pymongo.MongoClient()[config.mongo_db]

@app.route("/")
def index():
	url = request.args.get("url") if request.args.get("url") else ""
	category = request.args.get("category") if request.args.get("category") else ""
	return store(url, category)

def store_email_url(url,vars):
    conn[config.article].save({
   "media content": [{"url": image}],
   "_id":url,
   "source_name":domain,
   "links":[
      {
         "href":url,
         "type":"text/html",
         "rel":""
      }
   ],
   "source_table":"Article",
   "wfw_commentrss":"",
   "id":url,
   "slash_comments":" ",
   "published_parsed":"",
   "author":"",
   "comments":"",
   "content":[
      {
         "base":"",
         "type":"text/html",
         "value":content,
         "language":null
      }
   ],
   "title_detail":{
      "base":"",
      "type":"text/plain",
      "value":"",
      "language":null
   },
   "summary_detail":{
      "base":"",
      "type":"text/html",
      "value":"",
      "language":null
   },
   "tags":[
      {
         "term":"General",
         "scheme":null,
         "label":null
      }
   ],
   "timestamp":int(time.mktime(parse(article["published"]).timetuple())),
   "source_url":"",
   "link":"url",
   "authors":[
      {
         "name":""
      }
   ],
   "author_detail":{
      "name":""
   },
   "source_categories":[
      ""
   ],
   "source_content":"text",
   "summary":content,
   "guidislink":false,
   "published":"",
   "title":title
}
)

def store(url, category):
	feed = feedparser.parse(url)
	if len(feed["entries"]) > 0:
		connconn[config.mongo_col].save({.save({
			"_id": url,
		    "source_table": "Article",
			"source_name": feed["feed"]["title"],
			"source_url": url,
			"source_content": "text",
			"source_categories": category.split(",")
		})
		return '{"success": true}'
	else:
		content, title, domain, image=get_info_url(url)				 	
        	store_email_url(url,content, title, domain, image)
	return '{"success": false}'

app.run(host='0.0.0.0', port=5001, threaded=True)
