#!/usr/bin/python

lists = []
with open('foo.txt', 'r') as fo:
  for line in fo:
    lists.append(line.split(',')[0])
sorted_list = sorted(lists)
for item in sorted_list:
  print item


