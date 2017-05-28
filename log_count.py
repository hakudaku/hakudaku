#!/usr/bin/python -tt

import re
import sys
import os
import os.path

# Script for counting how many times a string appears in a file (e.g. log file) broken down by time, minute, or seconds
# The regex can be tweaked to customize the search string


def time(pattern, file_path):
  time_hash = {}
  f = open(file_path, 'rU')
  for line in f:
    match = re.search(pattern, line)
    if match:
      time = match.group(1)
      string = match.group(2)
      if string and not time in time_hash:
       time_hash[time] = 1
      elif string and time in time_hash:
        time_hash[time] = time_hash[time] + 1
  f.close()

  for key in sorted(time_hash.keys()):
    print key, time_hash[key]

def main():
  args = sys.argv[1:]

  if not args:
    print ('usage: [--hour|--minute|--second] --file <file_path>')
    sys.exit(1)
  
  hour_match = r'^\d\d\d\d-\d\d-\d\d\s+(\d\d)\S+(telus.net)'
  min_match = r'^\d\d\d\d-\d\d-\d\d\s+(\d\d:\d\d):\d\d\S+(telus.net)'
  sec_match = r'^\d\d\d\d-\d\d-\d\d\s+(\d\d:\d\d:\d\d)\S+(telus.net)'
  path = args[2]
  
  if os.path.exists(path):
    if args[0] == '--hour':
      time(hour_match, path)
    if args[0] == '--minute':
      time(min_match, path)
    if args[0] == '--second':
      time(sec_match, path) 
  else:
    print '%s does not exist' % path

if __name__ == '__main__':
  main()
