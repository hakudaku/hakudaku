#!/usr/bin/python -tt

import re
import sys

# Script for counting how many times a string appears in a file (e.g. log file) broken down by hour, minute, or seconds
# The regex can be tweaked to customize the search string

def hour(file_path):
  hour_hash = {}
  f = open(file_path, 'rU')
  for line in f:
    match = re.search(r'^\d\d\d\d-\d\d-\d\d\s+(\d\d)\S+(wp.pl)', line)
    if match:
      hour = match.group(1)
      string = match.group(2)
      if string and not hour in hour_hash:
       hour_hash[hour] = 1
      elif string and hour in hour_hash:
        hour_hash[hour] = hour_hash[hour] + 1 
  f.close()

  for key in sorted(hour_hash.keys()):
    print key, hour_hash[key]

def minute(file_path):
  minute_hash = {}
  f = open(file_path, 'rU')
  for line in f:
    match = re.search(r'^\d\d\d\d-\d\d-\d\d\s+(\d\d:\d\d):\d\d\S+(wp.pl)', line)
    if match:
      minute = match.group(1)
      string = match.group(2)
      if string and not minute in minute_hash:
       minute_hash[minute] = 1
      elif string and minute in minute_hash:
        minute_hash[minute] = minute_hash[minute] + 1
  f.close()

  for key in sorted(minute_hash.keys()):
    print key, minute_hash[key]

def second(file_path):
  second_hash = {}
  f = open(file_path, 'rU')
  for line in f:
    match = re.search(r'^\d\d\d\d-\d\d-\d\d\s+(\d\d:\d\d:\d\d)\S+(wp.pl)', line)
    if match:
      second = match.group(1)
      string = match.group(2)
      if string and not second in second_hash:
       second_hash[second] = 1
      elif string and second in second_hash:
        second_hash[second] = second_hash[second] + 1
  f.close()

  for key in sorted(second_hash.keys()):
    print key, second_hash[key]

def main():
  args = sys.argv[1:]

  if not args:
    print ('usage: [--hour|--minute|--second] --file <file_path>')
    sys.exit(1)

  if args[0] == '--hour':
    hour(args[2]) 
  if args[0] == '--minute':
    minute(args[2])
  if args[0] == '--second':
    second(args[2]) 

if __name__ == '__main__':
  main()
