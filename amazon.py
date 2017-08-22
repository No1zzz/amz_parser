# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style
import json
import copy
import io
import urllib
import fileinput

class AmazonBook:
    isEbook = False
    name = ''
    author = ''
    rank = ''
    avg_stars = ''
    num_reviews = ''
    price = ''
    pages = ''
    publisher = ''
    isbn = ''
    asin = ''
    publishDate = ''

def getBS_AmazonCOM(pages=1):
    bs_url = 'https://www.amazon.com/Best-Sellers-Beauty-Bath-Bathing-Accessories/zgbs/beauty/'

    for page in range(pages):
        r = requests.get(bs_url + 'ref=zg_bs_pg_' + str(page + 1) + '?_encoding=UTF8&pg=' + str(page + 1))
        soup = BeautifulSoup(r.text, 'lxml')
        Books = []
        for item in soup.findAll('div', {'class': 'zg_itemImmersion'}):
            b = AmazonBook()
            b.isEbook = True
            b.asin = json.loads(item.findAll('div', {'class': 'p13n-asin'})[0]['data-p13n-asin-metadata'])['asin']
            b.rank = item.findAll('span', {'class': 'zg_rankNumber'})[0].text.strip()
            b.name = item.findAll('img')[0]['alt']

            try:
                b.author = item.findAll('div', {'class': 'a-row'})[0].text.strip()
            except:
                pass

            try:
                icon_row = item.findAll('div', {'class': 'a-icon-row'})[0]
                b.avg_stars = icon_row.findAll(True, {'class': 'a-icon-star'})[0].text.strip()
                b.num_reviews = icon_row.findAll(True, {'class': 'a-size-small'})[0].text.strip()
            except:
                pass

            try:
                b.publishDate = item.findAll('div', {'class': 'zg_releaseDate'})[0].text
            except:
                pass

            Books.append(copy.copy(b))
        res = '\n'.join([book.asin for book in Books])
        print res
        with open('asin.txt', 'w') as f:
            f.write(res)

def getBS_AmazonIMG():

    with open('asin.txt') as f:
        for url in f:
            bs_url = 'https://www.amazon.com/dp/'+ url
            print bs_url
            r = requests.get(bs_url)
            soup = BeautifulSoup(r.text, 'lxml')
            img = []

            imgs = soup.find("div", {"id": "imgTagWrapperId"}).find("img")

            data = json.loads(imgs["data-a-dynamic-image"])

            filename = str(url) + '.jpg'
            x = 0

            for img in data:
                if x == 1:
                    print 'We got 1 image, skipping ' + url
                    s = open("asin.txt").read()
                    s = s.replace(url, '')
                    f = open("asin.txt", 'w')
                    f.write(s)
                    f.close()
                    exit
                else:
                    print 'Saved ' + img
                    x = x + 1
                    urllib.urlretrieve(img, filename)


#getBS_AmazonCOM()
getBS_AmazonIMG()
