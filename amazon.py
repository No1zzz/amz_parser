# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from colorama import Fore, Back, Style
import json
import copy
import io
import urllib
import fileinput
import time
import re

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

def getBS_AmazonCOM(pages=10):
    bs_url = 'https://www.amazon.com/Best-Sellers-Womens-Pumps/zgbs/fashion/679416011'

    for page in range(pages):
        #time.sleep (3)
        r = requests.get(bs_url + '/ref=zg_bs_pg_' + str(page + 1) + '?_encoding=UTF8&pg=' + str(page + 1))
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

        res = '\n'.join([book.asin for book in Books]) + '\n\t'
        print res
        with io.open('asin.txt', 'a+') as f:
            f.write(unicode(res))
        f.close()

def getBS_AmazonIMG():

    with open('asin.txt') as f:
        for url in f:
            time.sleep(3)
            bs_url = 'https://www.amazon.com/dp/'+ url.strip()
            print '\n' + 'New item'
            print bs_url + '\n'
            r = requests.get(bs_url)
            print r
            soup = BeautifulSoup(r.text, 'lxml')
            img = []

            imgs = soup.find("div", {"id": "imgTagWrapperId"}).find("img")

            data = json.loads(imgs["data-a-dynamic-image"])
            filename = url.strip() + '.jpg'
            x = 0

            for img in data:
                if x == 1:
                    print 'We already got image, skipping ' + url.strip()
                    s = open("asin.txt").read()
                    s = s.replace(url.rstrip(), '\r')
                    f = open("asin.txt", 'w')
                    f.write(s)
                    f.close()
                    exit
                else:
                    print 'Saved ' + img + '\n'
                    x = x + 1
                    urllib.urlretrieve(img, filename)

#getBS_AmazonCOM()
getBS_AmazonIMG()
