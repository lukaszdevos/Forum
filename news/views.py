from django.shortcuts import render
from news.models import NewsModel
from bs4 import BeautifulSoup
import requests
import urllib3





# Create your views here.

def scrape_news(request):
    urllib3.disable_warnings()
    session = requests.Session()
    
    url = 'https://trends.google.com/trends/trendingsearches/daily/rss?geo=PL'
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, 'html.parser')

    news = soup.find_all('item')

    articles = []
    i=1
    while i < 13:
        
        
        article = news[i]
        
        
        title  = article.find('title')
        link = article.find('ht:news_item_url')
        image = article.find('ht:picture')
        description = article.find('ht:news_item_snippet')
            
        new_article = NewsModel()
        
        new_article.pk = i
        new_article.topic = title.string
        new_article.url = link.string
        new_article.news_img = image.get_text()
        new_article.description = description.string.partition("&")[0]

        new_article.save()

        article = {
            'article_description': new_article.description,
            'article_image': new_article.news_img,
            'article_link': new_article.url,
            'article_title': new_article.topic,
        }

        articles.append(article)
        
        i+=1
    

    context = {
        'articles': articles
    }


    return render (request, "index.html", context)




