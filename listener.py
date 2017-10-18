import pymongo, config, feedparser, urllib, time
import bs4 as bs
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
app = Flask(__name__)
CORS(app)
conn = pymongo.MongoClient()[config.mongo_db]

@app.route("/")
def index():
	url = request.args.get("url") if request.args.get("url") else ""
	category = request.args.get("category") if request.args.get("category") else ""
	return store(url, category)

def store_email_url(url, content, title, domain, image):
   conn[config.article].save({
      "media content": [{
         "url": image
      }],
      "_id": url,
      "source_name": domain,
      "links":[{
         "href": url,
         "type": "text/html",
         "rel": ""
      }],
      "source_table": "Article",
      "wfw_commentrss": "",
      "id": url,
      "slash_comments": " ",
      "published_parsed": "",
      "author": "",
      "comments": "",
      "content": [{
         "base": "",
         "type": "text/html",
         "value": content,
         "language": None
      }],
      "title_detail": {
         "base": "",
         "type": "text/plain",
         "value": "",
         "language": None
      },
      "summary_detail": {
         "base": "",
         "type": "text/html",
         "value": "",
         "language": None
      },
      "tags":[{
         "term": "General",
         "scheme": None,
         "label": None
      }],
      "timestamp": int(time.time()),
      "source_url": "",
      "link": "url",
      "authors": [{
         "name": ""
      }],
      "author_detail":{
         "name": ""
      },
      "source_categories":[
         ""
      ],
      "source_content": "text",
      "summary": content,
      "guidislink": False,
      "published": str(datetime.now()),
      "title": title
   })

def find_nth(string, find_string, n):
    start = string.find(find_string)
    while start >= 0 and n > 1:
        start = string.find(find_string, start+len(find_string))
        n -= 1
    return start

def find_domain(url):
    start = url.find("http://")
    if start < 0:
        start = url.find("https://")
        start = start + len("https://")
    else:
        start = start + len("http://")
    end = find_nth(url, "/", 3)
    domain = url[start:end]
    return domain

def find_valid_image(soup):
    image=""
    #Try to find image by img attribute
    imagewithsize=soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("height")
                             and float(tag["height"]) >= 150.0)

    if len(imagewithsize) > 0:
        image=imagewithsize[0]

    else:
        imagewithsize = soup.findAll(lambda tag: tag.name == "img" and tag.has_attr("height"))

        if imagewithsize==0:
            print("no image")
        else:
            image=imagewithsize
        try:
            image=image['src']
        except:
            print(image)
    return image


def get_info_url(url):
    allcontent = []
    title=""
    image = ""
    domain=""
    try:
        source= urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(source, "lxml")
        print("soup: ", soup)
        for paragraph in soup.find_all('p'):
            content=paragraph.string   #content
            strcontent =str(content)
            allcontent += " " + strcontent
        domain = find_domain(url)  # domain
        try:
            domain= find_domain(url)
            title = soup.title.text
            image=find_valid_image(soup)
            image=image['src']
        except:
            pass


        return  allcontent,  domain, title,image
    except Exception as e:
        print("Error: ", e)
        return None, None, None, None


def store(url, category):
   feed = feedparser.parse(url)
   if len(feed["entries"]) > 0:
      conn[config.mongo_col].save({
			"_id": url,
		    "source_table": "Article",
			"source_name": feed["feed"]["title"],
			"source_url": url,
			"source_content": "text",
			"source_categories": category.split(",")
		})
      return '{"success": true}'
   else:
      content, title, domain, image = get_info_url(url)
      if content is not None:
         store_email_url(url, content, title, domain, image)
         return '{"success": true}'
   return '{"success": false}'

app.run(host='0.0.0.0', port=5001, threaded=True)
