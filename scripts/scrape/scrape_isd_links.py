# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 19:44:03 2014
Download, parse, and extract the relevant hyperlinks from a scholarship
database website
@author: tom
TODO: write in unicode (not ASCII)
"""

from bs4 import BeautifulSoup
import urllib3
from time import gmtime, strftime
import os
os.chdir('/home/tom/Desktop/scripts/python/isDB/scrape_and_parse/')
output = open('scholarship_urls.txt', 'w')

TOTAL_SEARCH_PAGES = 42
scholarship_urls = []

http = urllib3.PoolManager()
website = 'http://www.some_international_scholarship_database.com'
website_open_search = '/award/index?Award[fieldsOfStudy]=&Award[locations]' + \
                      '=&Award[details]=&Award[name]=&yt0=Search&Award_page='

for page_number in range(1, TOTAL_SEARCH_PAGES+1):
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    webpage = http.request('GET', website + website_open_search \
                           + str(page_number))
    
    soup = BeautifulSoup(webpage.data)
    links = soup.find_all('a')    
    
    complete_urls = [0]*len(links)    
    for i in range(len(links)):
        temp = links[i].get('href')
        if temp and temp[0] == '/' and len(temp) > 1 and temp[1].isdigit():    
            complete_urls[i] = website + temp
        else:
            complete_urls[i] = None
    
    scholarship_urls.extend(list(set(filter(None, complete_urls))))
    
for url in scholarship_urls:
    print >> output, url
output.close()
