#!/usr/bin/python -tt

import sys
import re
import os
import datetime
import commands
import shutil

switch_to_interface_dict = {}
interface_list = []
with open('switch_single.txt', 'r') as f:
    for line in f:
        match = re.search(r'(\S+net)\s+(.+)', line)
        if match:
            switch = match.group(1)
            interface = match.group(2)
            if switch not in switch_to_interface_dict:
                interface_list = [interface]
                switch_to_interface_dict[switch] = interface_list
            elif switch in switch_to_interface_dict: 
                interface_list.append(interface)
                switch_to_interface_dict[switch] = interface_list 


file_path = 'hosts.yaml'
for switch, interfaces in switch_to_interface_dict.iteritems():
    with open(file_path, 'r') as f:
        s = ':\n        master: nomon\n      '.join(interfaces)
        data = f.read()
        myreg = r'{0}.+?interfaces\:'.format(switch)
        match = re.search(myreg, data, re.DOTALL)
        data = data.replace(match.group(), match.group() + '\n' + '      ' + s + ':\n        master: nomon')
        with open(file_path, 'w') as f:
            f.write(data)

