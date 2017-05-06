#!/usr/bin/python -tt

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


# Merge data from individual files into a single file and remove duplicate data. 
def cat(weekly_path):
  weekly_hash = {}
  final_total = []
  filenames = os.listdir(weekly_path)
  with open(os.path.join(weekly_path, 'weekly.out'), 'w') as outfile:
    for f in filenames:
      with open(os.path.join(weekly_path, f)) as infile:
        outfile.write(infile.read())
    
  f = open(os.path.join(weekly_path, 'weekly.out'), 'rU')
  for line in f:
    match = re.search(r'^(\d\d\,\w\w\_\w+\,)(\d+)', line)
    if match:
      country = match.group(1)
      total = match.group(2)
      if not country in weekly_hash:
        weekly_hash[country] = total
  f.close()

  f = open(os.path.join(weekly_path, 'weekly_final.out'), 'w') 
  for key in weekly_hash.keys():
    (hour, binding, tot) = (key[0:2], key[3:], str(weekly_hash[key])) # Convert hash to tuples for custom sorting
    final_stats = (hour, binding, tot)
    final_total.append(final_stats)
  for x, y, z in sorted(final_total, key = operator.itemgetter(1, 0)): # Sort by binding, then by hour
    f.write(x)
    f.write(',')
    f.write(y)
    f.write(z)
    f.write('\n')
  f.close()
  print ('Data collection Complete. Final out file is' + ' ' + weekly_path + '/weekly_final.out')

# ssh into MTAs, drop the script on the MTA hosts, and run it 
def sftp(host):
  import paramiko, base64
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host)

  sftp = client.open_sftp()
  sftp.put('msys_get_weekly_stats.py', '/usr/tmp/msys_get_weekly_stats.py')
  sftp.close()
  client.close()
  
def ssh(hosts, cmd, weekly_path):
  print ('Gathering data...')
  from pssh import ParallelSSHClient
  client = ParallelSSHClient(hosts, channel_timeout=7200)
  try:
    output = client.run_command(cmd)
    client.join(output)
  except:
    for host in hosts:
      scp(host, weekly_path)
    cat(weekly_path)
  else:
    for host in hosts:
      scp(host, weekly_path)
    cat(weekly_path)
 
# Count/summarize weekly data for each hour
def copy_log(dir):
  now = time.time()
  hash = {}
  mainlog = []
  line_list = []
  weekly_totals = []
  filenames = os.listdir(dir)
  for f in filenames:
    match = re.search(r'mainlog.ec.\d+.bz2', f)
    if match and os.stat(os.path.join(dir, f)).st_mtime < now and os.stat(os.path.join(dir, f)).st_mtime > now - 14 * 86400:
      mainlog.append(os.path.join(dir, match.group()))
  logout = open('/usr/tmp/logs_processed', 'w')
  for log in mainlog:
    logout.write(log + '\n')
    bz_file = bz2.BZ2File(log)
    for line in bz_file.readlines():
      line_list.append(line.strip('\n'))
  for line in line_list:
    match = re.search(r'^\S+\s+(\d\d)\S+@(\w+commercial|\w+engaged)', line)  
    if match:
      hour = match.group(1) + match.group(2)
      delivery = re.search(r'@D@', line)
      temp_fail = re.search(r'@T@', line)
      reception = re.search(r'@R@', line)
      perm_fail = re.search(r'@P@', line)
      if delivery or temp_fail or reception or perm_fail:
        if not hour in hash:
          hash[hour] = 1
        else:
          hash[hour] = hash[hour] + 1
  status, output = commands.getstatusoutput("hostname -f")
  fname = output + '.' + 'out'
  f = open('/usr/tmp/' + fname, 'w')
  for key in hash.keys():
    (hour, country, total) = (key[0:2], key[2:], str(hash[key]))
    stats = (hour, country, total)
    weekly_totals.append(stats)
  for x, y, z in sorted(weekly_totals, key = operator.itemgetter(1, 0)):
    f.write(x)
    f.write(',')
    f.write(y)
    f.write(',')
    f.write(z)
    f.write('\n')
  f.close()

def main():
  hosts = []
  cmd = 'python /usr/tmp/msys_get_weekly_stats.py --local'
  args = sys.argv[1:]

  if not args:
    print ('usage: [--remote] [--local] -H <host_file>')
    sys.exit(1)
  
  if '-H' in args:
    host_file = args[2]
    f = open(host_file, 'rU')
    for line in f:
      hosts.append(line.strip('\n'))
  
  if args[0] == '--remote':
    weekly_path = os.path.expanduser('~') + '/msys_weekly_data/'
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
