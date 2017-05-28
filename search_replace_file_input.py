#!/usr/bin/python -tt

##If need to replace string with a different string for a bunch of files##
##Create a file and list all the filenames which need the search and replace of a string##
##The path variable will define the location of said filenames##
##The files list will have all the file names which  need the search and replace of a string##

import fileinput
import os
import sys

search_string = sys.argv[1]
replace_string = sys.argv[2]
path = sys.argv[3]
file_list = sys.argv[4]

files = []


file_h = open(file_list, 'rU')
for line in file_h:
  files.append(line.strip('\n'))

for f in files:
  for line in fileinput.input(f, inplace=True):
    line = line.rstrip().replace(search_string, replace_string)
    print line
