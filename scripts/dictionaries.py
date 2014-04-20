# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 18:20:35 2014
Get different dictionaries of words for scholarship text identification
Return list
@author: tom
"""

from bs4 import BeautifulSoup
import os
import mechanize

def common_words_5000():
    """
    Return a list of 5000+ common english words from a website
    """
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

def scholarship_words(filepath):
    """
    Returns a list of words from a text file scholarship_words.txt
    where the words are separated by commas
    Takes filepath as an argument
    """
    file_in = open(filepath)
    words = file_in.readlines()
    file_in.close()
    words = ' '.join(words)
    words = words.replace("\n", "")
    words = words.split(', ')
    return(words)


