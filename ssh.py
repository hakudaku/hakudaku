#!/usr/bin/python -tt

import sys
import re
from pssh import ParallelSSHClient
import paramiko, base64
import logging
from socket import gethostbyname, gaierror, timeout

def ssh(hosts, cmd):
  failed_hosts = []
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(hosts, timeout=5)
  output = client.run_command(cmd, stop_on_errors=False)
  for host in output:
    for line in output[host]['stdout']:
      print line
    print '\r'
    if output[host]['exception'] != None:
      print '***********Check Host %s. It is either down, invalid, or authentication failed*************\n' % (host)
    if output[host]['exit_code'] != 0:
      failed_hosts.append(host)
  if len(failed_hosts) > 0:
    print '***Hosts failed***'
  for host in failed_hosts:
    print host

def ssh2(host, cmd):
  failed_hosts = []
  try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, timeout=5)
    stdin, stdout, stderr = client.exec_command(cmd)
    for line in stdout:
      print line.strip('\n')
    for line in stderr:
      print line.strip('\n')
    print '\r'
    client.close()
  except (gaierror, timeout):
    print '***********Check Host %s. It is either down, invalid, or authentication failed*************\n' % (host)

def main():
  cmd = ''
  host = ''
  hosts = []
  args = sys.argv[1:]
  usage = ("usage: ssh.py -c cmd -h host. To specify a range of hosts, "
           "supported patterns are host[NUM-NUM] or host[NUM,NUM,NUM,...]. "
           "Examples:\nssh.py -c 'w' -h email-msys90.lup1\nssh.py -c 'w' -h "
           "email-msys[90-100].lup1\nssh.py -c 'w' -h email-msys[90,91,92,100,103].lup1")
  if not args:
    print usage
    sys.exit(1)
  if args[0] == '-c':
    cmd = 'hostname -f' + ';' + args[1]
  if args[2] == '-h':
    host = args[3]
  match_hyphen = re.search(r'^\S+\[\d+\-\d+\]', host)
  match_comma = re.search(r',', host)
  if match_hyphen:
    host_name = re.search(r'^(\S+)\[', host)
    host_colo = re.search(r'^\S+\[\S+](\S+)', host)
    num_match = re.search(r'(\d+)-(\d+)', host)
    int_1 = int(num_match.group(1))
    int_2 = int(num_match.group(2)) + 1
    for x in xrange(int_1,int_2):
      hosts.append(host_name.group(1) + str(x) + host_colo.group(1))
    if '--P' in args:
      ssh(hosts, cmd)
    else:
      for host in hosts:
       ssh2(host, cmd)
  elif match_comma:
    host_name = re.search(r'^(\S+)\[', host)
    host_colo = re.search(r'^\S+\[\S+](\S+)', host)
    num_match = re.findall(r'\W(\d+)', host)
    for num in num_match:
      hosts.append(host_name.group(1) + num + host_colo.group(1))
    if '--P' in args:
      ssh(hosts, cmd)
    else:
      for host in hosts:
       ssh2(host, cmd)
  elif '-H' in args:
    host_file = args[3]
    f = open(host_file, 'rU')
    for line in f:
      hosts.append(line.strip('\n'))
    if '--P' in args:
      ssh(hosts, cmd)
    else:
      for host in hosts:
       ssh2(host, cmd)
  else:
    ssh2(host, cmd)
   
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
