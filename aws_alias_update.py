#!/usr/bin/python

import json
import commands
import re 
import os
import fileinput

my_bash = os.path.expanduser('~') + '/.bashrc'
my_out_file = 'out.txt'

k8_master_cmd = 'aws ec2 describe-instances --filter "Name=tag-value,Values=*ubuntu1*"'
k8_node1_cmd = 'aws ec2 describe-instances --filter "Name=tag-value,Values=*ubuntu2*"'
k8_node2_cmd = 'aws ec2 describe-instances --filter "Name=tag-value,Values=*ubuntu3*"'

(status, master_json_out) = commands.getstatusoutput(k8_master_cmd)
(status, node1_json_out) = commands.getstatusoutput(k8_node1_cmd)
(status, node2_json_out) = commands.getstatusoutput(k8_node2_cmd)

# json output for master node
with open('data_file_master.json', 'w') as f:
    f.write(master_json_out)

# json output for worker node 1
with open('data_file_node1.json', 'w') as f:
    f.write(node1_json_out)

# json output for worker node 2
with open('data_file_node2.json', 'w') as f:
    f.write(node2_json_out)

# get master node ip
with open('data_file_master.json', 'r') as f:
    match = re.findall(r'PublicDnsName.+(ec2.+)"', f.read())
    master_node_ip_current = match[0]

# get node1 ip
with open('data_file_node1.json', 'r') as f:
    match = re.findall(r'PublicDnsName.+(ec2.+)"', f.read())
    node1_ip_current = match[0]

# get node2 ip
with open('data_file_node2.json', 'r') as f:
    match = re.findall(r'PublicDnsName.+(ec2.+)"', f.read())
    node2_ip_current = match[0]

# if line in .bashrc matches the regexs, do the replace operation, else copy line as is
with open(my_bash, 'r') as fin:
    with open(os.path.expanduser('~') + '/' + my_out_file, 'w') as fout: 
        for line in fin:
            match1 = re.search(r'ubuntu1.+(ec2.+)"', line)
            match2 = re.search(r'ubuntu2.+(ec2.+)"', line)
            match3 = re.search(r'ubuntu3.+(ec2.+)"', line)
            if match1:
                string_to_replace = match1.group(1)
                fout.write(line.replace(string_to_replace, master_node_ip_current))
            elif match2:
                string_to_replace = match2.group(1)
                fout.write(line.replace(string_to_replace, node1_ip_current))
            elif match3:
                string_to_replace = match3.group(1)
                fout.write(line.replace(string_to_replace, node2_ip_current))
            else:
                fout.write(line)


# Rename out file to .bashrc
os.rename(os.path.expanduser('~') + '/' + my_out_file, my_bash)
