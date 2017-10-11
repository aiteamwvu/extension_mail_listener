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
    allcontent = []
    try:
        source= urllib.request.urlopen(url)
        soup = bs.BeautifulSoup(source, "lxml")
        for paragraph in soup.find_all('p'):
            content=paragraph.string   #content
            strcontent =str(content)
            #print("strcontent ", strcontent)

            allcontent.append(strcontent)

        for e in allcontent:
            print("", e)
        domain=find_domain(url)       #domain
        title=soup.title.text          #title




        image=soup.findAll('img')[0].get("src") #get the first image
        return  allcontent, title, domain, image
    except Exception as e:
        print("Error: ", e)




