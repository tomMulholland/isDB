# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 19:56:14 2014
## Import html text, parse out headers, <p>, and <a> in order
## write to a single .csv file with the "999filename" as identifier
## BENCHMARKING
## Before Parallel Python, takes 6 minutes 15 seconds
## After Parallel Python, takes 1 minute 6 seconds
## 5.68 times faster - overhead lowers efficiency

# TODO
## This runs in the Spyder interpreter, but the command raises an IO error
@author: tom
"""

import os
os.chdir('/home/tom/deepdive/app/isDB/scripts')
from dictionaries import common_words_5000
os.chdir('/home/tom/deepdive/app/isDB/data')
#from bs4 import BeautifulSoup
from time import gmtime, strftime
import re
import csv
import pp

## Function to clean the text
def clean_text(string_in):
    string_in = string_in.replace("\\n", "").replace("\\t", "")
    string_in = string_in.replace("\\", " ").replace("\\r", "")
    string_out = string_in.replace("[", "")
    return(string_out)

## Function to pass to workers
## fileset is a list of file names
## tag_matches is an re object with the tags we want from the Soup
## word_dict is a dictionary of English words        
def clean_file(fileset, tag_matches, word_dict):
    
    from bs4 import BeautifulSoup
    result_set =[]
    
    ## A function for checking if the string contains characters a-z
    import re
    check = re.compile(r'[a-z]').search
    
    ## Open the file, make the Soup
    for filename in fileset:
        file_in = open("linkto/" + filename, 'r')
        soup = BeautifulSoup(' '.join(file_in.readlines()))
        file_in.close()
        
        ## Extract the text lines, format them
        i = 0
        all_text = 1000*[0]
        #for item in soup.stripped_strings:
        for item in soup.find_all(tag_matches):
            i += 1          
            if ("script" in item.name):
                temp = 0
            elif item.string is None:
                temp = 0
            else:
                temp = item.string
                temp = temp.encode('ascii', 'replace')
                temp = clean_text(temp)
            
            ## Make sure the text contains characters a-z
            if (temp != 0) and not bool(check(temp)):
                temp = 0
            ## Make sure the text doesn't contain css or http
            if (temp != 0) and ("http" in temp):
                temp = 0
            if (temp != 0) and ("css" in temp):
                temp = 0
                
            ## Check if the text contains one of the dictionary words
            contains_word = False
            word_index = 0
            if (temp != 0):
                while (contains_word == False and (word_index < len(word_dict))):
                    if ((" " + word_dict[word_index] + " ") in temp):
                        contains_word = True
                    word_index += 1
            
            if contains_word == False:
                temp = 0
            
            ## Add non-zero entries to the text list
            if temp == 0:
                pass
            elif i < len(all_text):
                all_text[i] = temp
            else:
                all_text.append(temp)
            
        ## Remove all zeros and shorten the vector
        all_text = filter(lambda a: a != 0, all_text)
        result_set.append(' '.join(all_text))
    
    return([fileset, result_set])
                    
################################################                    
    
# MAIN SCRIPT    
## Initialize some values
start_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
filenames = os.listdir(os.getcwd() + "/linkto") # directory with html files
run_number = 0

## Get the 5000 most common English words from
## http://www.englishclub.com/vocabulary/common-words-5000.htm
## uses the script get_common_words.py
word_dict = common_words_5000()
word_dict.extend(["GPA", "TOEFL", "SAT", "GRE"])
tag_matches = re.compile(r'a{1}|p{1}|h[0-9]')

## Set up the workers (parallelize the job)
job_server = pp.Server()
num_cpus = job_server.get_ncpus() 
print("Using " + str(num_cpus) + " CPUs")
jobs = []
set_len = len(filenames) // num_cpus

for i in range(num_cpus):
    if i < (num_cpus - 1):
        file_set = filenames[i * set_len : (i + 1) * set_len]
    else:
        file_set = filenames[i * set_len: ]
    jobs.append(job_server.submit(clean_file, 
                                  (file_set, tag_matches, word_dict), 
                                  depfuncs=(clean_text, )))
                                  #modules=(,)))
## Organize the results                
results = []
for job in jobs:
    results.append(job())        
all_results = []
file_names = []
for names, result in results:
    all_results.extend(result)
    file_names.extend(names)
 
## Write the results to .csv
csv_file = open("link_to.csv", 'w')
writer = csv.writer(csv_file, delimiter=',')  
for i in range(len(file_names)):
    writer.writerow(["999" + file_names[i].replace(".html", "")] + \
                    [all_results[i]])      
csv_file.close()

## Get performance
end_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("Start Time: " + start_time)
print("End Time: " + end_time)
