import bs4 as bs
import urllib.request


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

def get_info_url(url):

    try:
        source= urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(source, "lxml")
        print("domain ",find_domain(url))        #domain
        title=soup.title.text          #title
        print(title)

        for paragraph in soup.find_all('p'):
            content=paragraph.string   #content
            print(content)
        print(soup.findAll('img')[0].get("src")) #get the first image
    except Exception as e:
        print("Error: ", e)

url="https://gizmodo.com/amazons-sick-high-end-kindle-got-a-serious-overhaul-1819330183"


get_info_url(url)
