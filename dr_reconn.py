#!/usr/bin/python

import os
import sys
import commands
import re
import shutil
import glob

my_home_dir = os.path.expanduser('~')

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
os.chdir(my_home_dir)
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

# Reindex Documents from GCIDS
os.chdir(my_home_dir)
my_edis_missing_dr_csv = '{}/input/edis_missing_dr.csv'.format(my_home_dir)
my_edis_missing_pr_csv = '{}/input/edis_missing_pr.csv'.format(my_home_dir)
my_reindex_script = '/data1/ReindexRecordCreator/FromGCIDReindexRecordCreator.py'
my_missing_DR_path = '/home/sysops/GARBAGE/edis/MissinginDR/'
my_missing_PR_path = '/home/sysops/GARBAGE/edis/MissinginPR/'
if not os.path.exists(my_reindex_script):
    print '{} does not exist. Exiting!'.format(my_reindex_script)
    sys.exit(1)

if os.path.isdir(my_home_dir + '/input'):
    pass
else:
    os.mkdir(my_home_dir + '/input')
my_input_dir = '{}/input'.format(my_home_dir)
my_missing_dr_files = glob.glob(my_missing_DR_path + '*.csv')
my_missing_pr_files = glob.glob(my_missing_PR_path + '*.csv')
dr_id_list = []
pr_id_list = []

for myfile in my_missing_dr_files:
    with open(myfile, 'r') as f:
        for line in f:
            caseid = line.split(',')
            dr_id_list.append(caseid[0])
with open(my_edis_missing_dr_csv, 'w') as fw:
    for i in dr_id_list:
        fw.write(i + '\n')

for myfile in my_missing_pr_files:
    with open(myfile, 'r') as f:
            for line in f:
                caseid = line.split(',')
                pr_id_list.append(caseid[0])
with open(my_edis_missing_pr_csv, 'w') as fw:
    for i in pr_id_list:
        fw.write(i + '\n')

my_cmd = 'python {} {} out_file'.format(my_reindex_script, my_input_dir)
os.system(my_cmd)

my_dr_outfile = '{}/out_file1.json'.format(my_home_dir)
my_pr_outfile = '{}/out_file2.json'.format(my_home_dir)

mongo_import_cmd_dr = 'mongoimport --host fab-apdr01-karafui-h2-1 --port 23758 --ssl --sslAllowInvalidCertificates -u "admin" -p  "AcTmOnGoIaNcE0014" --authenticationDatabase "admin" --db prodapac --collection reindex_gcid --file {} --type json'.format(my_dr_outfile)

mongo_import_cmd_pr = 'mongoimport --host fab-apac01-karafui-h1-1 --port 23758 --ssl --sslAllowInvalidCertificates -u "admin" -p  "AcTmOnGoIaNcE0014" --authenticationDatabase "admin" --db prodapac --collection reindex_gcid --file {} --type json'.format(my_pr_outfile)

os.system(mongo_import_cmd_dr)
os.system(mongo_import_cmd_pr)
