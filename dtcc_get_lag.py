#!/usr/bin/python

import os
import subprocess
from pymongo import MongoClient

# Authenticate to api.sys.prod.smarsh.cloud
auth_cmd = 'cf login -a api.sys.prod.smarsh.cloud -u vineet.bhatia@smarsh.com -p 1w@ntt0fuckpr3m@n@r@y@n -s alcatraz-mt-prod'
os.system(auth_cmd)

# SSL forward
process = subprocess.Popen('cf ssh admin-app-mt -L 23758:10.40.1.44:23758 -T', shell=True)


uri = 'mongodb://admin:AcTmOnGoIaNcE0014@localhost:23758/?ssl=true&ssl_cert_reqs=CERT_NONE'

myclient = MongoClient(uri)

mydb = myclient["dtccprod"]
mycol = mydb["archive_metrics"]

myquery = { "processing_state": "Queued" }

mydoc = mycol.find(myquery)
my_doc_count = mydoc.count()

print my_doc_count

process.kill()
