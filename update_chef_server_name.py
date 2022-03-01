#!/usr/bin/env python

import argparse
import re
import os
import shutil

# Update chef URL in /etc/chef/client.rb file

def update_chef(replacement_chef_name):
    homedir = os.path.expanduser('~')
    chef_client_file = '/etc/chef/client.rb'
    shutil.copy(chef_client_file, homedir) # Make copy of client.rb before doing any writes to the original file
    with open(chef_client_file, 'r') as f:
        file_content = f.read()
    current_chef_name_match = re.search(r'https://(\S+\.authentic8\.com)', file_content)
    new_file_content = file_content.replace(current_chef_name_match.group(1), replacement_chef_name)
    with open(chef_client_file, 'w') as f:
        f.write(new_file_content)


def main():
    parser = argparse.ArgumentParser(description="Update chef URL in client.rb")
    parser.add_argument("new", help="new chef server name")

    args = parser.parse_args()
    replacement_chef_name = args.new

    update_chef(replacement_chef_name)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
