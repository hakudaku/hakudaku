#!/usr/bin/python -tt

"""
Calculate total soft soft bounces
The original script here searches 10 days of the inband_bounce.csv logs on MTAs
Prints out count of "10 Invalid Recipient" errors that occurred in last 10 days
for all MTAs combined referenced in hosts file.
"""

import sys
import re
import time
import os
import bz2
import commands
import operator

# scp files from MTAs to local box
def scp(host, weekly_path):
  import paramiko, base64
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host)

  sftp = client.open_sftp()
  sftp.get('/usr/tmp/' + host + '.' + 'out', weekly_path + host + '.' + 'out')
  sftp.close()

def tot(weekly_path):
  abs_path = []
  total = []
  filenames = os.listdir(weekly_path)
  for file in filenames:
    abs_path.append(os.path.join(weekly_path, file))
  for file in abs_path:
    with open(file) as f:
      for line in f:
        match = re.search(r'\s+(\d+)', line)
        total.append(match.group(1))
  total = map(int, total) # Convert strings to ints in the 'total' list. The sum function below on strings will cause error.
  print sum(total)


# ssh into MTAs, drop the script on the MTA hosts, and run it 
def sftp(host):
  import paramiko, base64
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host)

  sftp = client.open_sftp()
  sftp.put('msys_get_bounce.py', '/usr/tmp/msys_get_bounce.py')
  sftp.close()
  client.close()
  
def ssh(hosts, cmd, weekly_path):
  print ('Gathering data...')
  from pssh.clients import ParallelSSHClient
  client = ParallelSSHClient(hosts, channel_timeout=3600)
  try:
    output = client.run_command(cmd)
    client.join(output)
  except:
    for host in hosts:
      scp(host, weekly_path)
    tot(weekly_path)
  else:
    for host in hosts:
      scp(host, weekly_path)
    tot(weekly_path)
 
# Count/summarize data
def copy_log(dir):
  now = time.time()
  hash = {}
  bouncelog = []
  line_list = []
  filenames = os.listdir(dir)
  for f in filenames:
    match = re.search(r'inband_bounce.csv.\d+.bz2', f)
    if match and os.stat(os.path.join(dir, f)).st_mtime < now and os.stat(os.path.join(dir, f)).st_mtime > now - 10 * 86400:
      bouncelog.append(os.path.join(dir, match.group()))
  logout = open('/usr/tmp/bounce_logs_processed', 'w')
  for log in bouncelog:
    logout.write(log + '\n')
    bz_file = bz2.BZ2File(log)
    for line in bz_file.readlines():
      line_list.append(line.strip('\n'))
  for line in line_list:
    match = re.search(r'10 Invalid Recipient', line)
    if match:
      count = match.group()
      if not count in hash:
        hash[count] = 1
      else:
        hash[count] = hash[count] + 1
  status, output = commands.getstatusoutput("hostname -f")
  fname = output + '.' + 'out'
  f = open('/usr/tmp/' + fname, 'w')

  for key in hash.keys():
    f.write(key)
    f.write(':')
    f.write(' ' )
    f.write(str(hash[key]))
    f.write('\n')
  f.close()

def main():
  hosts = []
  cmd = 'python /usr/tmp/msys_get_bounce.py --local'
  args = sys.argv[1:]

  if not args:
    print ('usage: msys_get_bounce.py --remote -H <host_file>')
    sys.exit(1)
  
  if '-H' in args:
    host_file = args[2]
    f = open(host_file, 'rU')
    for line in f:
      hosts.append(line.strip('\n'))
  
  if args[0] == '--remote':
    weekly_path = os.path.expanduser('~') + '/msys_bounce_data/'
    if not os.path.exists(weekly_path):
      os.makedirs(weekly_path)
    ssh(hosts, cmd, weekly_path)
  
  if args[0] == '--scp':
    for host in hosts:
      print (host)
      scp(host, weekly_path)

  if args[0] == '--final':
    cat(weekly_path)

  if args[0] == '--sftp':
    for host in hosts:
      sftp(host)
  
  elif args[0] == '--local':
    copy_log('/var/log/ecelerity')

if __name__ == '__main__':
  main()
