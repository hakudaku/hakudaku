#!/usr/bin/env python

import commands
import sys
import time
import os


def update_ttl(zone_file, domain):
    zone_list = []
    with open(zone_file, 'r') as f:
        for line in f:
            remove_new_line_char = line.strip()
            
            zone_list.append(remove_new_line_char)
    for record in zone_list:
        cmd = "cli53 rrcreate --replace {} '{}'".format(domain, record)
        os.system(cmd)    

def main():
    args = sys.argv[1:]
    usage = ('update_ttl.py [file] [domain]')
    if not args or len(args) < 2:
        print usage
        sys.exit(1)
    zone_file = args[0]
    domain = args[1]
    update_ttl(zone_file, domain)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
