#!/usr/bin/python -tt

f = open('test1', 'rU')
my_list = []
for l in f:
  my_list.append(l.split())
for l in my_list:
  print l[1]
