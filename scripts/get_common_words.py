# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 18:20:35 2014
Get the 5000 most common English words
Return list
@author: tom
"""

from bs4 import BeautifulSoup
import os
import mechanize

def get_words():
    
    os.chdir('/home/tom/deepdive/app/isDB/data')
    url = "http://www.englishclub.com/vocabulary/common-words-5000.htm"
    
    request = mechanize.Request(url)
    response = mechanize.urlopen(request)
    html_response = response.readlines()
    response.close()
    soup = BeautifulSoup(' '.join(html_response))
    tagged_words = soup.find_all('li')    
    words = len(tagged_words)*[0]
    i = 0    
    
    for word in tagged_words:
        words[i] = word.string.encode('ascii')
        i += 1
    
    return(words)
