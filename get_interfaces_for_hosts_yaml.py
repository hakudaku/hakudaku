#!/usr/bin/python

import commands
import re
import os
import sys

my_id_dict = {} 
my_switch_list = []
my_inw_switch_file = os.path.expanduser('~') + '/inw_switches'
os.mknod(os.path.expanduser('~') + '/switch.txt')
my_file = os.path.expanduser('~') + '/switch.txt'

with open(my_inw_switch_file, 'r') as f:
    for line in f:
        my_switch_list.append(line.strip('\n'))
        

for switch in my_switch_list:
    snmpwalk_descr_cmd = 'snmpwalk -v 2c -c r0ck3tfu31# {0} descr'.format(switch)
    (status, output) = commands.getstatusoutput(snmpwalk_descr_cmd)
    match = re.findall(r'STRING:\s+(.+)', output)
    if match:
        my_id_dict[switch] = match



with open(my_file, 'w') as f:
    for k, dk in my_id_dict.iteritems():
        for x in dk:
             f.write('{0} {1}\n'.format(k, x))
