#!/usr/bin/env python

list_of_removed_hosts = []
with open('ass', 'r') as f:
    for line in f:
        #new_line = line.strip('\n')
        list_of_removed_hosts.append(line)

with open('ass1', 'r') as f:
    with open('prod_new', 'a') as f2:
        for line in f:
            if line in list_of_removed_hosts:
                pass
            else:
                f2.write(line)

