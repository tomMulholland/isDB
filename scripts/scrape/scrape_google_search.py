# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 19:44:31 2014
http://stackoverflow.com/questions/7746832/scraping-and-parsing-google-search-results-using-python
@author: not tom
"""


import time, random
from xgoogle.search import GoogleSearch, SearchError
import os

os.chdir('/home/tom/Desktop/scripts/python/isd/scrape_and_parse')

f = open('urls.txt','wb')

for i in range(0,5):
    wt = random.uniform(3, 4)
    gs = GoogleSearch("university financial aid")
    gs.results_per_page = 100
    gs.page = i
    results = gs.get_results()
    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    print 'This is the %dth iteration and waited %f seconds' % (i, wt)
    for res in results:
        f.write(res.url.encode("utf8"))
        f.write("\n")

print "Done"
f.close()
