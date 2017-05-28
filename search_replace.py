#!/usr/bin/python -tt

##If need to replace string with a different string for a bunch of files##
##Create a file and list all the filenames which need the search and replace of a string##
##The path variable will define the location of said filenames##
##The files list will have all the file names which  need the search and replace of a string##

#import fileinput
import os
import sys

files = []
path = raw_input('Dir path: ')
while not os.path.exists(path):
  print "The path %s does not exist" % path
  path = raw_input('Dir path: ')
filename = raw_input('file which contains the list of filenames to be updated: ')
search_string = raw_input('search_string: ')
replace_string = raw_input('replace_string: ')
f = open(filename, 'rU')

for line in f:
  files.append(line.strip('\n'))

for f in files:
  yml_file = open(os.path.join(path, f), 'r')
  data = yml_file.read()
  if not search_string in data:
    print 'search_string %s not found in filename %s' % (search_string, f) 
  data = data.replace(search_string, replace_string)
  yml_file = open(os.path.join(path, f), 'w')
  yml_file.write(data)
