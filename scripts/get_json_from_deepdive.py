#! /usr/bin/env python
"""Get json objects from deepdive"""
#import psycopg2
import json
import fileinput

json_objects = []
# For each sentence
for row in fileinput.input():
    sentence_obj = json.loads(row)
    json_objects.append(sentence_obj) 

j = json.dumps(json_objects)
objects_file = '/home/tom/deepdive/app/isDB/data/schol_text_objects.js'
f = open(objects_file,'w')
print >> f, j
