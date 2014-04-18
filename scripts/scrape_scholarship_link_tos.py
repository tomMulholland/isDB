# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 10:04:11 2014
Using downloaded scholarship files, scrape the text from the links
given on the scholarship page, which may or may not be scholarship text
@author: tom
"""

from time import gmtime, strftime
#from codecs import register_error
import os
import mechanize
from urllib2 import HTTPError, URLError
start_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))

os.chdir('/home/tom/Desktop/scripts/python/isDB/scrape_and_parse/')

filenames = os.listdir(os.getcwd() + "/scholarships")

run_number = 0
missing_or_broken = []

for filename in filenames:
    
    ## Let's time this bad boy
    run_number += 1    
    print("\nCurrent run: " + str(run_number))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    ## The last line of the files is a URL to the original page
    file_in = open("scholarships/" + filename, 'r')
    lines = file_in.readlines()
    url = lines[len(lines)-1].replace("\n", "")
    file_in.close()
    
    ## Test if the file includes a URL
    if not (url.startswith("http")): 
        missing_or_broken.append(filename)
    ## Open URL, save HTML to file
    else:           
        ## Using mechanize to access the pages
        ## Catch HTTPError 404 (page not found)
        try:
            request = mechanize.Request(url.replace("\n", ""))
            response = mechanize.urlopen(request)
            html_response = response.readlines()
            response.close()
            
            dir_prefix = "linkto/"
            output = open(dir_prefix + filename + ".html", 'w')
        
            for item in html_response:
                print >> output, item
        
            output.close()
            
        except (HTTPError, URLError):
            missing_or_broken.append(filename)     

## Keep track of the missing or broken urls
output = open("missing_or_broken_urls.txt", 'w')
for item in missing_or_broken:
    print >> output, item

output.close()

end_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("Start Time: " + start_time)
print("End Time: " + end_time)
