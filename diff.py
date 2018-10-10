#!/usr/bin/python

import difflib
import re

s = 'abcd'
t = 'abcdef'

d = difflib.Differ()
diff = d.compare(s, t)
for line in diff:
  match = re.search(r'^\+\s+(.+)', line)
  if match:
    print match.group(1)
#print '\n'.join(diff) 
