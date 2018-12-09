#!/Users/vineetbhatia/ENV/bin/python -tt

import re

with open('_sudoers.erb', 'rU') as in_file:
    buf = in_file.read()
    match = re.search(r'(nagios ALL.*)(\s+%.*)', buf)
    if match:
        buf = buf.replace(match.group(), match.group(1) + '\n' +  'nagios ALL=(root) /usr/local/bin/new_script' + match.group(2))
        with open('_sudoers.erb', 'w') as out_file:
            out_file.write(buf)
