# 2
# link- https://blog.intigriti.com/category/bugbytes/

'''
Articles to be fetched won't be crossing 1 page in what I am implementing
'''

# imports
import os
import datetime

# external imports
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup
import requests, json

# DB setup
URI = os.getenv('MONGODB_URL')
client = MongoClient(URI)
db = client['hackArticles']
bug_bytes_articles = db['bug_bytes_articles']


# Bot send message function
def send_message(WEB_HOOK, message):
    send = requests.post(WEB_HOOK, data=json.dumps({ "content": message }), headers={ 'Content-Type': 'application/json',})
    
    return send.status_code

##################################################################SCRAPER CODE####################################
'''
url
scraper
result
'''
articles = [] # nested list of [title, url]

URL = 'https://blog.intigriti.com/category/bugbytes/'

def scraper():
    html = requests.get('https://blog.intigriti.com/category/bugbytes/').text
    page_soup = soup(html, 'html.parser')

    site_name = page_soup.title.text
    
    raw_articles = page_soup.findAll('h2', class_='blog-entry-title')

    for raw_article in raw_articles[:3]:
        articles.append([raw_article.a.text, raw_article.a['href']])

    message = {
        'site_name': site_name,
        'articles': articles[::-1]
    }

    return message

def result(WEB_HOOK, CHAT_ID):
    try:
        articles = scraper().get('articles')
        for article in articles:
            if bug_bytes_articles.find_one({'title': article[0], 'CHAT_ID':CHAT_ID}) is None: # add in the database and send to telegram
                bug_bytes_articles.insert_one({
                    'title': article[0],
                    'url': article[1],
                    'CHAT_ID': CHAT_ID,
                    "date": datetime.datetime.utcnow()
                })

                message = article[1]
                print(send_message(WEB_HOOK, message))

    except Exception as e:
        print('[!] Failure for bug bytes articles')
        print(str(e))

##################################################################SCRAPER CODE####################################