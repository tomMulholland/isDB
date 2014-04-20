# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 13:52:39 2014

@author: tom
"""

for index in i_keyword:
        #Make a phrase with the four->0 words before and 0->four words after
        for i in range(1, 5, 1):
            for j in range(1, 5, 1):
                
                
                
                
   for index in i_keyword:
        #Make a phrase with the four->0 words before and 0->four words after
        for i in range(1, 5, 1):
            for j in range(1, 5, 1):
    while True:
        sublist = i_keyword[start_index:]
        next_phrase = list(itertools.takewhile(lambda x: (x[1] in ["ORGANIZATION"]), sublist))
        if next_phrase:
            phrases_indicies.append([x[0] for x in next_phrase])
            start_index = next_phrase[-1][0] + 1
        elif start_index == len(ner_list)+1: break
        else: start_index = start_index + 1
    
    
      # Output a tuple for each PERSON phrase
#    for phrase in phrases_indicies:
#        print >> output, "sentence_id: " + str(row1["id"])
#        print >> output,"start_index:" + str(phrase[0])
#        print >> output,"length:" + str(len(phrase))
#        print >> output,"text:" + " ".join(row1["words"][phrase[0]:phrase[-1]+1])
#        print >> output,"document id:" + str(row1["document_id"])

#output.close()






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
                