# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 12:41:19 2014
## Pass text files to a single .csv file
## The filename is the ID in the first column
## All the text is placed together in the second column
@author: tom
"""

import os
os.chdir('/home/tom/deepdive/app/isDB/data')
import csv
from time import gmtime, strftime

start_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
filenames = os.listdir(os.getcwd() + "/scholarships")

csv_file = open("scholarships.csv", 'w')
writer = csv.writer(csv_file, delimiter=',')

for filename in filenames:
    file_in = open("scholarships/" + filename, 'r')
    lines = file_in.readlines()
    file_in.close()

    writer.writerow([filename] + \
                    [' '.join(lines)])      


csv_file.close()

## Get performance
end_time = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))
print("Start Time: " + start_time)
print("End Time: " + end_time)