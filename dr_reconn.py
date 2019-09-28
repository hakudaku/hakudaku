#!/usr/bin/python

import os
import sys
import commands
import re
import shutil
import glob

# Run for Primary site

# Check needed scripts are present
my_paths = ['/data1/ES_Scripts/ES_DUMP/ES_DUMP_ediscovery.py', '/data1/ES_DR_Scripts/ES_DR_DUMP/ES_DUMP_ediscovery.py', '/data1/MissingGCID/pyspark/batch_diff_gcid.py', '/data1/MissingGCID/pyspark/gcid_reconReport.py']

for path in my_paths:
    if os.path.exists(path):
        print '{} exists'.format(path)
    elif not os.path.exists(path):
        print '{} does not exist! Exiting!!'.format(path)
        sys.exit(1)


# Create edisconfig.ini with the current caseids
my_l = []
f = open('case_ids_apac', 'rU')
for line in f:
    line = line.strip()
    my_l.append(line)
ids = ','.join(my_l)
ids = 'caseids = {}'.format(ids)

my_edisconfig_path = '/data1/ES_Scripts/ES_DUMP/edisconfig.ini'
f = open(my_edisconfig_path, 'r')
for line in f:
    match = re.search(r'caseids.+', line)
    if match:
        f = open(my_edisconfig_path, 'r')
        data = f.read()
        data = data.replace(match.group(), ids)
        f = open(my_edisconfig_path, 'w')
        f.write(data)
        f.close()

# Clear existing folders from outputediscovery dir
my_dirs = glob.glob('/data1/ES_Scripts/ES_DUMP/outputediscovery/*')
for dir in my_dirs:
    shutil.rmtree(dir)

# Run ES_DUMP_ediscovery.py
os.chdir('/data1/ES_Scripts/ES_DUMP/')
os.system('python /data1/ES_Scripts/ES_DUMP/ES_DUMP_ediscovery.py')

# Consolidate cvss with case ids
os.chdir('/data1/ES_Scripts/ES_DUMP/outputediscovery/')
os.system('for i in `ls -1`;do cat $i/*.csv > Pri_${i}.csv;done') 

# Clear data from ediscovery dir and move Pri* files to it
my_files = glob.glob('/data1/ES_CSVS/ediscovery/*.csv')
for f in my_files:
    os.remove(f)
os.chdir('/data1/ES_Scripts/ES_DUMP/outputediscovery/')
my_pri_csv_files = glob.glob('Pri*')
for f in my_pri_csv_files:
    shutil.move(f, '/data1/ES_CSVS/ediscovery')


# Run above for DR site

# Create edisconfig.ini with the current caseids
my_l = []
os.chdir('/home/VBhatia')
f = open('case_ids_apac', 'rU')
for line in f:
    line = line.strip()
    my_l.append(line)
ids = ','.join(my_l)
ids = 'caseids = {}'.format(ids)

my_edisconfig_path = '/data1/ES_DR_Scripts/ES_DR_DUMP/edisconfig.ini'
f = open(my_edisconfig_path, 'r')
for line in f:
    match = re.search(r'caseids.+', line)
    if match:
        f = open(my_edisconfig_path, 'r')
        data = f.read()
        data = data.replace(match.group(), ids)
        f = open(my_edisconfig_path, 'w')
        f.write(data)
        f.close()

# Clear existing folders from outputediscovery dir
my_dirs = glob.glob('/data1/ES_DR_Scripts/ES_DR_DUMP/outputediscovery/*')
for dir in my_dirs:
    shutil.rmtree(dir)

# Run ES_DUMP_ediscovery.py
os.chdir('/data1/ES_DR_Scripts/ES_DR_DUMP/')
os.system('python /data1/ES_DR_Scripts/ES_DR_DUMP/ES_DUMP_ediscovery.py')

# Consolidate cvss with case ids
os.chdir('/data1/ES_DR_Scripts/ES_DR_DUMP/outputediscovery/')
os.system('for i in `ls -1`;do cat $i/*.csv > DR_${i}.csv;done') 

# Clear data from ediscovery dir and move Pri* files to it
my_files = glob.glob('/data1/ES_DR_CSVS/ediscovery/*.csv')
for f in my_files:
    os.remove(f)
os.chdir('/data1/ES_DR_Scripts/ES_DR_DUMP/outputediscovery/')
my_dr_csv_files = glob.glob('DR_*')
for f in my_dr_csv_files:
    shutil.move(f, '/data1/ES_DR_CSVS/ediscovery')


#Take difference
os.chdir('/data1/MissingGCID/pyspark/')
os.system('python batch_diff_gcid.py')
