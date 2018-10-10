#!/usr/bin/env python -tt

import re
import sys
import os

def log_parse(log_file, pattern, string_to_match, increment):
  
  # check if path exists
  if not os.path.exists(log_file):
    print "%s does not exist!!" % log_file
    sys.exit(1)

  dict = {}
  f = open(log_file, 'r')
  for line in f:
    match = re.search(pattern, line)
    if match:
      time = match.group(1)
      if time not in dict:
        dict[time] = 1
      else:
        dict[time] = dict[time] + 1
  f.close()
  
  if increment == 's':
    print 'Matching string "%s", broken down by second...' % string_to_match

  elif increment == 'm':
    print 'Matching string "%s", broken down by minute...' % string_to_match

  elif increment == 'h':
    print 'Matching string "%s", broken down by hour...' % string_to_match
 
  for key in sorted(dict.keys()):
    print key, dict[key]       

def main():
  args = sys.argv[1:]
  usage = ('log_count_test.py |-h|-m|-s| --file <file_path> --string <string to match>')
  if not args or len(args) < 5:
    print usage
    sys.exit(1)


  string_to_match = args[4]
  log_file = args[2] 
  hour_match_regex = r'^(\w\w\w\s\d\d\s\d\d):\d\d:\d\d.+(%s)' % string_to_match
  minute_match_regex = r'^(\w\w\w\s\d\d\s\d\d:\d\d):\d\d.+(%s)' % string_to_match
  second_match_regex = r'^(\w\w\w\s\d\d\s\d\d:\d\d:\d\d).+(%s)' % string_to_match

  if args[0] == '-h':
    log_parse(log_file, hour_match_regex, string_to_match, 'h')
  elif args[0] == '-m':
    log_parse(log_file, minute_match_regex, string_to_match, 'm')
  elif args[0] == '-s':
    log_parse(log_file, second_match_regex, string_to_match, 's')
  else:
    print usage
    sys.exit(1)
  
# This is the standard boilerplate that calls the main() function.

if __name__ == '__main__':
  main()
