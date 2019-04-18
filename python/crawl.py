import requests
from bs4 import BeautifulSoup
import pymysql

def saverec(nurl,ntitle,nfrom,ndate,ncount,ncontent):
    db = pymysql.connect("localhost", "root", "chengyiyi422", "news")
    cursor = db.cursor()
    sql = """INSERT INTO cucnews(newsurl,title,newsfrom,newsdate,contents,newscount) \
         VALUES('%s','%s','%s','%s','%s','%s')""" % (nurl, ntitle, nfrom, ndate, pymysql.escape_string(ncontent), ncount)
    try:
        cursor.execute(sql)

        print("ok")
        db.commit()
    except:
        print(db.error())
        db.rollback()
    db.close()

kv = {'user-agent': 'Mozilla/5.0'}
for i in range(1, 428):
    url = 'http://by.cuc.edu.cn/zcyw/' + str(i)
    page = requests.get(url, headers=kv)
    page.encoding = page.apparent_encoding
    s = BeautifulSoup(page.text, 'html.parser')
    title = s.find_all('h3', attrs={'class', 'tit'})
    for t in title:
        newsurl = t.find_all('a')
        #print(newsurl)
        urllen = str(newsurl[0]).find('target')
        tarurl = str(newsurl[0])[9:urllen - 2]
        #print(tarurl)
        #print(t.get_text())
        #url = "http://www.cuc.edu.cn/zcyw/11584.html"
        r = requests.get(tarurl, headers=kv)
        soup = BeautifulSoup(r.text, 'html.parser')
        #爬虫莫名其妙不成功了，其实是对的

        stitle = soup.find_all('h1')
        newsfrom = soup.find_all('sapn')
        newsdate = soup.find_all('sapn')
        viewcount = soup.find_all('span', attrs={'id': 'hits'})
        newscontent = soup.find_all('article', attrs={'class', 'con-area'})

        if len(stitle):
            stitle = stitle[0].get_text()
        else:
            continue

        info = newsfrom[0].get_text()
        #print(info)
        info = info.replace(' ', '').replace("&nbsp", '').replace("来源：", '').replace("浏览量：", '')
        #info = info.strip()

        #print(info.split())
        #print(info[-78: -68])
        newfrom = info.split()[0]
        newdate = info.split()[1]


        newcount = viewcount[0].get_text()
        newcontent = newscontent[0].get_text()
        #saverec(tarurl, stitle, newfrom, newdate, newcount, newcontent)
