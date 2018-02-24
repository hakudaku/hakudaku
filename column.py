#!/usr/bin/python -tt

f = open('test2', 'rU')
my_list = []
for l in f:
  my_list.append(l.split())
sorted_list = sorted(my_list)
for l in sorted_list:
  print l[0]
