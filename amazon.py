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
import random
import os

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
    bs_url = 'https://www.amazon.com/Best-Sellers-Beauty-Bathing-Accessories/zgbs/beauty/11056491'

    for page in range(pages):
        time.sleep (3)
        r = requests.get(bs_url + '/ref=zg_bs_pg_' + str(page + 1) + '?_encoding=UTF8&pg=' + str(page + 1))
        soup = BeautifulSoup(r.text, 'lxml')
        Books = []
        for item in soup.findAll('div', {'class': 'zg_itemImmersion'}):
            b = AmazonBook()
            b.isEbook = True
            b.asin = json.loads(item.findAll('div', {'class': 'p13n-asin'})[0]['data-p13n-asin-metadata'])['asin']
            b.rank = item.findAll('span', {'class': 'zg_rankNumber'})[0].text.strip()

            try:
                b.pr = item.findAll('span', {'class': 'p13n-sc-price'})[0].text.strip('$')
                b.pri = int(float(b.pr))
                b.price = str(b.pri)
            except IndexError:
                a = random.randint(1, 10)
                b.price = str(a)
                print a
                print 'oops'


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
        res_price = '\n'.join([book.price for book in Books]) + '\n\t'
        with io.open('asin.txt', 'w') as f:
            f.write(unicode(res))
        f.close()

        with io.open('price.txt', 'w') as f:
            f.write(unicode(res_price))
        f.close()

def getBS_AmazonIMG():

    with open('asin.txt') as f:
        lines = (line.rstrip() for line in f)
        lines = (line for line in lines if line)
        for url in lines:
            time.sleep(3)
            bs_url = 'https://www.amazon.com/dp/'+ url.strip()
            print '\n' + 'New item'
            print bs_url + '\n'
            r = requests.get(bs_url)
            print r
            soup = BeautifulSoup(r.text, 'lxml')
            img = []

            try:
                imgs = soup.find("div", {"id": "imgTagWrapperId"}).find("img")
            except AttributeError:
                print '\n' + 'Images loading fail. Maybe block from Amazon?' + '\n'
            data = json.loads(imgs["data-a-dynamic-image"])
            x = 0

            for img in data:
                if x == 1:
                    print 'We already got image, skipping ' + url.strip()
                    exit
                else:
                    fl = random.randint(1,18)
                    add_fl = str(fl)
                    filename = str(fl) + '.jpg'
                    print filename
                    x = x + 1
                    if os.path.exists(filename):
                        print 'OwowowWOwowowowowowowowowo'
                        print 'Saving with new name'
                        filename_add = add_fl + '(' + add_fl + ')' + '.jpg'
                        urllib.urlretrieve(img, filename_add)
                        print 'Saved ' + img + ' in ' + filename_add + ' \n'
                    else:
                        urllib.urlretrieve(img, filename)


                    s = open("asin.txt").read()
                    s = s.replace(url.rstrip(), '\r')
                    f = open("asin.txt", 'w')
                    f.write(s)
                    f.close()

getBS_AmazonCOM()
getBS_AmazonIMG()
