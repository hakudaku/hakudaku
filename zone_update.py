#!/usr/bin/python3

import os
import re
import subprocess

bind_restart_cmd = '/etc/init.d/bind9 restart'
my_home_dir = os.path.expanduser('~')
my_bind_conf = '/etc/bind/db.teeniv.me'
my_tmp_file = '{}/bin/tmp'.format(my_home_dir)
my_get_ip_cmd = 'ec2metadata | grep public-ipv4'
output = subprocess.check_output(my_get_ip_cmd, shell=True) 
output_str_format = str(output)
match = re.search(r'(\d+\.\d+\.\d+\.\d+)', output_str_format)
new_ip = match.group(1)

with open(my_bind_conf, 'r') as fr:
    with open(my_tmp_file, 'w') as fw:
        for line in fr:
            my_serial_match = re.search(r'(\d+).+Serial', line)
            my_ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            if my_ip_match:
                string_to_replace = my_ip_match.group(1)
                fw.write(line.replace(string_to_replace, new_ip))
            elif my_serial_match:
                serial_to_replace = int(my_serial_match.group(1))
                new_serial = serial_to_replace + 1
                serial_to_replace_str = str(serial_to_replace)
                new_serial_str = str(new_serial)
                fw.write(line.replace(serial_to_replace_str, new_serial_str))
            else:
                fw.write(line)

os.rename(my_tmp_file, my_bind_conf)

# Restart bind
os.system(bind_restart_cmd)
