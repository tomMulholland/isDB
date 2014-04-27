#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script takes a postgreSQL table as input, reads the json, and
extracts relationships that may indicate the text refers to a scholarship

A relation will be created for every mention of each word in the dictionary
and writes the number of mentions to each dictionary word with the index to
a JSON object.

@author: tomMulholland
"""

import fileinput
import json
import os
from nltk.stem.porter import PorterStemmer
from nltk.corpus import names
#import pp
proj_dir = "/home/tom/deepdive/app/isDB"

# Job function
def find_mentions(objects, dictionary, name_dict, stemmer):
    word_range = 5
    w_arnd = "words_around="
    json_results = []
    for text_obj in objects:
        try:
            text = text_obj['text'].split(' ')
            text_indices = []
            dict_indices = []
            for text_ind in range(len(text)):
                word_norm = stemmer.stem(text[text_ind]).lower()   
                for dict_ind in range(len(dictionary)):
                    if word_norm == dictionary[dict_ind]:
                        text_indices.append(text_ind)
                        dict_indices.append(dict_ind)
            list_occur = []
            
            # Get the number of occurrences of dictionary words
            for dict_index in list(set(dict_indices)):
                count = dict_indices.count(dict_index)
                list_occur.append(dictionary[dict_index] + \
                                        "=" + str(count))
            
            list_occur.append("total_dict_occur=" + str(len(dict_indices)))
                
        # Output a tuple for each PERSON phrase
            for index in range(len(text_indices)):
                word_index = text_indices[index]
                if (word_index - word_range) > 0:
                    five_before = word_index - word_range
                else:
                    five_before = 0
                if (word_index + word_range) < len(text):
                    five_after = word_index + word_range
                else:
                    five_after = len(text) - 1
                list_occur.append(w_arnd + ' '.join(
                                text[five_before:five_after + 1]))
                list_occur.append(w_arnd + ' '.join(
                                text[word_index:five_after + 1]))
                list_occur.append(w_arnd + ' '.join(
                                text[five_before:word_index + 1]))
                for name in name_dict:
                    if (name in text[five_before:word_index + 1]):
                        list_occur.append("first_name_before_" + \
                                          dictionary[dict_indices[index]]\
                                          + "=True")
                        break
                
            for entry in list_occur:
                json_results.append(json.dumps({
                    "text_id": text_obj['id'],
                    "feature": entry
                }))
        # Catch objects with no 'text' field
        except KeyError: 
            pass
    return(json_results)
    
# Get the data passed from DeepDive
data = []
for row in fileinput.input():
  data.append(json.loads(row))

## Get json file; when not using DeepDive
#json_data=open(proj_dir + '/data/web_text_objects.js')
#data = json.load(json_data)
#json_data.close()

# Get scholarship words dictionary    
os.chdir(proj_dir + "/scripts")
from dictionaries import scholarship_words
schol_dict = scholarship_words(proj_dir + "/scripts/scholarship_words.txt")
 
# Stem the scholarship dictionary
stemmer = PorterStemmer()
schol_dict_stm = []
for word in schol_dict:
    schol_dict_stm.append(stemmer.stem(word).lower())
    
# Eliminate duplicates
schol_dict_stm = list(set(schol_dict_stm))

# Get list of names
name_dict = names.words()

# Create parallel python objects
#job_server = pp.Server()
#num_cpus = job_server.get_ncpus() 
#print("Using " + str(num_cpus) + " CPUs")
#jobs = []
#set_len = len(data) // num_cpus
#"""TRYING TO START THE JOBS"""
## Divide the dictionary of json objects among the CPUs
#for i in range(num_cpus):
#    if i < (num_cpus - 1):
#        data_set = data[i * set_len : (i + 1) * set_len]
#    else:
#        data_set = data[i * set_len: ]
#    jobs.append(job_server.submit(find_mentions, 
#                                  (data_set, schol_dict_stm, name_dict, stemmer),
#                                  modules=("json",)))

# Collect the results                            
#results = []
#for job in jobs:
#    results.extend(job())        
results = find_mentions(data, schol_dict_stm, name_dict, stemmer)

# Output to a text file; when not using DeepDive
#output = open(proj_dir + "/data/dict_web_mentions.txt", 'w')
#for item in results:
#    print >> output, item
#output.close()

# Print lines to DeepDive file
for line in results:
    print(line)
    
