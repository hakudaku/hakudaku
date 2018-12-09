#!/usr/bin/python -tt

import sys
import re
import os
import commands

# ssh into MTAs and drop the script in /usr/tmp dir
def sftp(host):
  import paramiko, base64
  client = paramiko.SSHClient()
  client.load_system_host_keys()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host)

  sftp = client.open_sftp()
  sftp.put('queue_per_binding.py', '/usr/tmp/queue_per_binding.py')
  sftp.close()
  client.close()

def ssh(hosts, cmd):
  from pssh.clients import ParallelSSHClient
  client = ParallelSSHClient(hosts, channel_timeout=3600)
  output = client.run_command(cmd)
  client.join(output)

# iterate thru binding.conf file, grab all the bindings, and get the total queue for each binding
def total_queue(file):
  bindings = []
  f = open(file, 'rU')
  for line in f:
    match = re.search(r'binding\s+"(\S+)"', line)
    if match:
      bindings.append(match.group(1))
  for b in bindings:
    print b + ':'
    binding_sum_cmd = 'echo' + ' ' + '"' + 'binding summary' + ' ' + b + '" | sudo /opt/msys/ecelerity/bin/ec_console | grep "Total Queue Size"'
    binding_aqueue_cmd = 'echo' + ' ' + '"' + 'binding' + ' ' + 'active' ' ' + b + ' ' + '1' + '"' + ' ' + """| sudo /opt/msys/ecelerity/bin/ec_console  | grep -v 'Total:' | awk {'printf ("%5s\\t%s\\n",  $2, $6)'}"""
    binding_dqueue_cmd = 'echo' + ' ' + '"' + 'binding' + ' ' + 'delayed' ' ' + b + ' ' + '1' + '"' + ' ' + """| sudo /opt/msys/ecelerity/bin/ec_console  | grep -v 'Total:' | awk {'printf ("%5s\\t%s\\n",  $2, $8)'}"""
    bind_sum = commands.getoutput(binding_sum_cmd)
    bind_aqueue = commands.getoutput(binding_aqueue_cmd)
    bind_dqueue = commands.getoutput(binding_dqueue_cmd)
    print bind_sum + '\n' + 'Active queue domains:' + '\n' + bind_aqueue + '\n' + 'Delayed queue domains:' + '\n' + bind_dqueue


def main():
  hosts = []
  cmd = 'python /usr/tmp/queue_per_binding.py --local'
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
    ssh(hosts, cmd)

  
  if args[0] == '--sftp':
    for host in hosts:
      sftp(host)

  elif args[0] == '--local':
    total_queue('/opt/msys/ecelerity/etc/conf/default/includes/binding.conf')

if __name__ == '__main__':
  main()
