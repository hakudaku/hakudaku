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
ticket_count = 169
column_count = 41

with open(home_dir + '/scripts/data_type', 'r') as f:
    for line in f:
        line = line.strip('\n')
        data_type_to_ticket_dict[line] = [ticket_count, column_count]
        ticket_count = ticket_count + 1
        column_count = column_count + 1

for key in data_type_to_ticket_dict.keys():
    repo.git.checkout('main')
    repo.remotes.origin.pull()
    branch_name = 'LMSD-{}-create-data-ingestion-script-for-data-type-{}'.format(data_type_to_ticket_dict[key][0], key)
    new_data_type_file_name = '{}{}'.format(key, file_ext)
    #my_new_branch = repo.create_head(branch_name)
    repo.git.checkout(branch_name)
    #my_new_branch.checkout()
    print repo.active_branch
    with open('band.sh', 'r') as f:
        with open(new_data_type_file_name, 'w') as fw:
            for line in f:
                match1 = re.search(r'Jose.Salas', line)
                match2 = re.search(r'Authors:\s+(.+)', line) 
                match3 = re.search(r'Update\s+(\$2)', line)
                match4 = re.search(r'Example:\s+(\$2)', line)
                match5 = re.search(r'Band', line)
                if match1:
                    fw.write(line.replace(match1.group(), 'Vineet.Bhatia'))
                elif match2:
                    fw.write(line.replace(match2.group(1), 'Vineet'))
                elif match3:
                    fw.write(line.replace(match3.group(1), '$' + str(data_type_to_ticket_dict[key][1])))
                elif match4:
                    fw.write(line.replace(match4.group(1), '$' + str(data_type_to_ticket_dict[key][1])))
                elif match5:
                    fw.write(line.replace(match5.group(), key))
                else:
                    fw.write(line)
    repo.git.add(data_ingestion_dir + new_data_type_file_name)
    repo.git.commit('-m', 'LMSD-' + str(data_type_to_ticket_dict[key][0]) + ' ' + 'Updates ' + new_data_type_file_name + ' script')
    repo.git.push("origin", branch_name)
    
