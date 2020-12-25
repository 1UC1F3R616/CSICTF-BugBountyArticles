# 1
# link- https://portswigger.net/research/articles

'''

'''

# imports
import os
import datetime
from pymongo import MongoClient
from bs4 import BeautifulSoup as soup
import requests, json

# DB setup
URI = os.getenv('MONGODB_URL')
client = MongoClient(URI)
db = client['hackArticles']
portswigger_research_articles = db['portswigger_research_articles']


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
BASE_URL = 'https://portswigger.net'

articles = [] # nested list of [title, url]
def scraper():
    html = requests.get('https://portswigger.net/research/articles').text
    page_soup = soup(html, 'html.parser')

    site_name = page_soup.title.text
    
    raw_articles = page_soup.findAll('a', class_='noscript-post') # only 4 on latest page

    for raw_article in raw_articles[:2]: # They add articles very rarely, even total will be 4 and I am taking 2 only
        articles.append([raw_article.span.text, BASE_URL + raw_article['href']])

    message = {
        'site_name': site_name,
        'articles': articles[::-1]
    }

    return message

def result(WEB_HOOK, CHAT_ID):
    try:
        articles = scraper().get('articles')
        for article in articles:
            if portswigger_research_articles.find_one({'title': article[0], 'CHAT_ID':CHAT_ID}) is None: # add in the database and send to telegram
                portswigger_research_articles.insert_one({
                    'title': article[0],
                    'url': article[1],
                    'CHAT_ID': CHAT_ID,
                    "date": datetime.datetime.utcnow()
                })

                message = article[1]
                print(send_message(WEB_HOOK, message))

    except Exception as e:
        print('[!] Failure for portswigger research articles')
        print(str(e))

##################################################################SCRAPER CODE####################################