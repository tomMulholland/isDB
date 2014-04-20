# -*- coding: utf-8 -*-
"""
This script takes a postgreSQL table as input, reads the json, and
extracts relationships that may indicate the text refers to a scholarship

A relation will be created for every mention of each word in the dictionary
and writes the number of mentions to each dictionary word with the index to
a JSON object.

@author: tomMulholland
"""

import json
import os
from nltk.stem.porter import *

# Get scholarship words dictionary    
proj_dir = "/home/tom/deepdive/app/isDB"
os.chdir(proj_dir + "/scripts")
from dictionaries import scholarship_words
schol_dict = scholarship_words(proj_dir + "/scripts/scholarship_words.txt")

# Stem the scholarship dictinary
stemmer = PorterStemmer()
schol_dict_stm = []
for word in schol_dict:
    schol_dict_stm.append(stemmer.stem(word).lower())
    
# Eliminate duplicates
schol_dict_stm = list(set(schol_dict_stm))

# Get json file
os.chdir(proj_dir + "/data")
json_data=open('web_text_objects.js')
data = json.load(json_data)
json_data.close()

output = open("dict_web_mentions.txt", 'w')

for text_obj in data:
    i_keyword = []
    text = text_obj['text'].split(' ')
    text_indices = []
    dict_indices = []
    for text_ind in range(len(text)):
        word_norm = stemmer.stem(text[text_ind]).lower()   
        for dict_ind in range(len(schol_dict_stm)):
            if word_norm == schol_dict_stm[dict_ind]:
                text_indices.append(text_ind)
                dict_indices.append(dict_ind)
# Output a tuple for each PERSON phrase
    for ind in range(len(text_indices)):
        print output, json.dumps({
            "text_id": text_obj['id'],
            "mention_index": text_indices[ind],
            "text_word": text[text_indices[ind]],            
            "dict_word": schol_dict_stm[dict_indices[ind]]
        })


output.close()



#from pprint import pprint
#pprint(data[0])

# Find phrases that are tagged with PERSON
#  phrases_indicies = []
#  start_index = 0
#  ner_list = list(enumerate(sentence_obj["ner_tags"]))
#  while True:
#    sublist = ner_list[start_index:]
#    next_phrase = list(itertools.takewhile(lambda x: (x[1] in ["PERSON"]), sublist))
#    if next_phrase:
#      phrases_indicies.append([x[0] for x in next_phrase])
#      start_index = next_phrase[-1][0] + 1
#    elif start_index == len(ner_list)+1: break
#    else: start_index = start_index + 1
#        print json.dumps({
#        "sentence_id": row1["id"],
#        "start_index": phrase[0],
#        "length": len(phrase),
#        "text": " ".join(row1["words"][phrase[0]:phrase[-1]+1])
#    })



#import psycopg2
# TAKEN FROM psycopg2 DOCS
# Connect to an existing database
#conn = psycopg2.connect("dbname=isDB user=tom")
#
## Open a cursor to perform database operations
#cur = conn.cursor()
#
## Query the database and obtain data as Python objects
#cur.execute("SELECT * FROM schol_sentences;")
#rows = cur.fetchall()
#
## Close communication with the database
#cur.close()
#conn.close()
#
#j = json.dumps(json_objects)
#objects_file = '/home/tom/Desktop/schol_sentence_objects.js'
#f = open(objects_file,'w')
#print >> f, j
# 
#""" SHOULD HAVE WRITTEN THE FILE""" 
#cur.close()
#conn.close()
