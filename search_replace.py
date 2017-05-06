import fileinput
import os

files = []
path = '/Users/vbhatia/ops-config/hosts'

f = open('dev_hosts_dns_correct', 'rU')
for line in f:
  files.append(line.strip('\n'))

for f in files:
  yml_file = open(os.path.join(path, f), 'r')
  data = yml_file.read()
  data = data.replace('10.20.3.33', '10.20.10.53')
  yml_file = open(os.path.join(path, f), 'w')
  yml_file.write(data)
