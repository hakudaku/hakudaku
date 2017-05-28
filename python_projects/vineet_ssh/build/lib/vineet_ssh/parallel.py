from pssh import ParallelSSHClient
import logging

def ssh_parallel(hosts, cmd):
  failed_hosts = []
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(hosts)
  output = client.run_command(cmd, stop_on_errors=False)
  for host in output:
    for line in output[host]['stdout']:
      print line
    print '\n'
    if output[host]['exception'] != None:
      print '***********Check Host %s. It is either down, invalid, or authentication failed*************\n' % (host)
    if output[host]['exit_code'] != 0:
      failed_hosts.append(host)
  if len(failed_hosts) > 0:
    print '***Hosts failed***'
  for host in failed_hosts:
    print host
