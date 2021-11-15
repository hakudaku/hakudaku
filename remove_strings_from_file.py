#!/usr/bin/env python
#
# Compare file1 and file2. Final file3 will have all lines from file2 minus lines in file1.

list_of_removed_hosts = []
with open('file1', 'r') as f:
    for line in f:
        #new_line = line.strip('\n')
        list_of_removed_hosts.append(line)

with open('file2', 'r') as f:
    with open('file3', 'a') as f2:
        for line in f:
            if line in list_of_removed_hosts:
                pass
            else:
                f2.write(line) # only write lines NOT in file1 to the new file (file3)

