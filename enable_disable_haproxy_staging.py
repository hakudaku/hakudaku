import os
import sys
from pssh.clients import ParallelSSHClient
import logging

def snc(haproxy_snc, cmd, bg, backend):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(haproxy_snc)
  client.run_command(cmd, stop_on_errors=False)
  for h in haproxy_snc:
    if 'disable' in cmd:
      print 'On proxy %s, %s is set to MAINT mode for %s!' % (h, backend, bg)
    elif 'enable' in cmd:
      print 'On proxy %s, %s is set to ACTIVE mode for %s!' % (h, backend, bg)

def main():
  args = sys.argv[1:]
  if not args or len(args) < 3:
    print 'Usage: haproxy_enable_disable.py [ACTION] [COLO] [CLUSTER]'
    print 'Example: haproxy_enable_disable.py [enable|disable] [snc|dub|snc] [c1|c2|c3|c4]'
    sys.exit(1)     
  path = '/usr/local/lib/haproxyctl/haproxyctl'
  haproxyctl = os.path.abspath(path)

  haproxy_snc = ['mta-haproxy100-staging.snc1', 'mta-haproxy101-staging.snc1']

  msys_group_snc_c1 = {}
  msys_group_snc_c1['msys_mx'] = ['email-msys100-staging']
  msys_group_snc_c1['msys_co'] = ['email-msys100-staging']
  msys_group_snc_c1['msys_cl'] = ['email-msys100-staging']
  msys_group_snc_c1['msys_pe'] = ['email-msys100-staging']

  msys_group_snc_c2 = {}
  msys_group_snc_c2['msys_mx'] = ['email-msys101-staging']
  msys_group_snc_c2['msys_co'] = ['email-msys101-staging']
  msys_group_snc_c2['msys_cl'] = ['email-msys101-staging']
  msys_group_snc_c2['msys_pe'] = ['email-msys101-staging']

  if args[1] == 'snc' and args[2] == 'c1':
    for bg in msys_group_snc_c1.keys():
      for backend in msys_group_snc_c1[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        snc(haproxy_snc, cmd, bg, backend)

  if args[1] == 'snc' and args[2] == 'c2':
    for bg in msys_group_snc_c2.keys():
      for backend in msys_group_snc_c2[bg]:
        cmd = 'sudo %s %s server %s/%s' % (haproxyctl, args[0], bg, backend)
        snc(haproxy_snc, cmd, bg, backend)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
