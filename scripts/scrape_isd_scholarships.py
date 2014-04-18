# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 10:04:11 2014
Download, parse, and extract the relevant data from a scholarship
database website
@author: tom
"""

from bs4 import BeautifulSoup
from time import gmtime, strftime
#from codecs import register_error
from os import chdir
start_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
chdir('/home/tom/Desktop/scripts/python/isDB/scrape_and_parse/')

file_in = open('scholarship_urls.txt', 'r')
urls = file_in.readlines()
file_in.close()
chdir('/home/tom/Desktop/scripts/python/isDB/scrape_and_parse/scholarships')        

#Let's login to the website
import mechanize

website_url = 'http://www.some_international_scholarship_database.com'
authentication_url = website_url + '/site/login'
request = mechanize.Request(authentication_url)
response = mechanize.urlopen(request)
forms = mechanize.ParseResponse(response, backwards_compat=False)
response.close()
form = forms[0]
form["LoginForm[username]"] = "your_username"
form["LoginForm[password]"] = "your_password"
request2 = form.click()
response2 = mechanize.urlopen(request2)
html_output = response2.readlines()
response2.close()
run_number = 0

#We're logged in, now let's open a page


for url in urls:
    run_number += 1    
    print("\nCurrent run: " + str(run_number))
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    request3 = mechanize.Request(url.replace("\n", ""))
    response3 = mechanize.urlopen(request3)
    
    
    #Make a Soup, and extract the things we want
    soup = BeautifulSoup(response3)
    headers = soup.find_all('h2') + soup.find_all('h4')
    title = headers[0].get_text().strip().encode('ascii', 'replace')
    text = soup.find_all('p')
    
    length1 = 12
    length2 = 6
    temp_results = [0]*(length1 + length2)
    
    temp_results[0] = ('\n' + headers[0].get_text().strip() + '\n')\
        .encode('ascii', 'replace')
    
    for i in range(1, length1 - 1):
        temp_results[i] = ('\n' + headers[i].get_text().strip() + '\n' \
                           + text[i+1].get_text().strip())\
                           .encode('ascii', 'replace')     
    
    temp_results[11] = (headers[11].get_text().strip()  + '\n').\
        encode('ascii', 'replace')
        
    headers = soup.find_all('th')
    text = soup.find_all('td')
    
    for i in range(length2 - 1):
        temp_results[i + length1] = \
            ('\n' + headers[i].get_text().strip() + '\n'\
            + text[i].get_text().strip()).encode('ascii', 'replace')
    
    try:    
        temp_results[length1 + length2 - 1] =\
            ('\n' + headers[length2 - 1].get_text().strip() + '\n'\
            + website_url + text[length2 - 1].contents[0].get('href'))\
            .encode('ascii', 'replace')
    except IndexError:
        temp_results.pop(length1 + length2 - 1)
        
    ind1 = url.rfind("/")
    ind2 = url[:ind1].rfind("/")
    file_name = url[ind2+1:ind1]
    
    output = open(file_name, 'w')

    for item in temp_results:
        print >> output, item

    output.close()

end_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("Start Time: " + start_time)
print("End Time: " + end_time)
