#!/usr/bin/python

# Open a file
f = open("foo.txt", "r")
for x in f:
  print x, 

f = open("foo.txt", "r")
f.seek(0,2)
for x in f:
  print x,
