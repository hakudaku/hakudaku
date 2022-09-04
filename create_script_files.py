#!/usr/bin/env python

import argparse
import commands
import re
import os
import git
import time

data_type_to_ticket_dict = {}
home_dir = os.path.expanduser('~')
docker_repo = '{}/git_repos/docker'.format(home_dir)
data_ingestion_dir = '{}/git_repos/docker/Monitoring_Scripts/Data_Ingestion/'.format(home_dir)
repo = git.Repo(docker_repo)
file_ext = '.sh'
os.chdir(data_ingestion_dir)
count = 169

with open('data_type', 'r') as f:
    for line in f:
        line = line.strip('\n')
        data_type_to_ticket_dict[line] = count
        count = count + 1

for key in data_type_to_ticket_dict.keys():
    repo.git.checkout('main')
    branch_name = 'LMSD-{}-create-data-ingestion-script-for-data-type-{}'.format(data_type_to_ticket_dict[key], key)
    new_data_type_file_name = '{}{}'.format(key, file_ext)
    my_new_branch = repo.create_head(branch_name)
    my_new_branch.checkout()
    print repo.active_branch
    with open('band.sh', 'r') as f:
        with open(new_data_type_file_name, 'w') as fw:
            for line in f:
                fw.write(line.replace('Band', key))
    repo.git.add(data_ingestion_dir + new_data_type_file_name)
    repo.git.commit('-m', 'LMSD-' + data_type_to_ticket_dict[key] + ' ' + 'Added initial ' + new_data_type_file_name + ' script')
    repo.git.push("origin", branch_name)
    
