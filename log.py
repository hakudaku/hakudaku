import re
with open('error', 'r') as fo:
    for line in fo:
        match = re.search(r'error', line, re.IGNORECASE)
        if match:
            print 'match'
        else:
            print 'no'
