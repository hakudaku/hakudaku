#!/usr/bin/python

import json
import commands
import re 
import os
import fileinput
import sys

my_bash = os.path.expanduser('~') + '/.bashrc'
my_out_file = 'out.txt'

my_cmd = 'aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicDnsName" --output=text'

(status, out) = commands.getstatusoutput(my_cmd)


# if line in .bashrc matches the regexs, do the replace operation (only if ip has changed), else copy line as is
with open(my_bash, 'r') as fin:
    with open(os.path.expanduser('~') + '/' + my_out_file, 'w') as fout: 
        for line in fin:
            match = re.search(r'(ec2.+)"', line)
            if match:
                if match.group(1) == out:
                    print 'IP has not changed. Nothing to do.'
                    sys.exit(1)
                if match.group(1) != out:
                    string_to_replace = match.group(1)
                    fout.write(line.replace(string_to_replace, out))
            else:
                fout.write(line)


# Rename out file to .bashrc
os.rename(os.path.expanduser('~') + '/' + my_out_file, my_bash)

# Re-read .bashrc
output = commands.getoutput('source' + ' ' + my_bash)
