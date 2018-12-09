#!/usr/bin/env -tt

import sys
import re
from pssh.clients import ParallelSSHClient
import paramiko, base64
import logging

def ssh(host, fpm_cmd):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(host)
  output = client.run_command(fpm_cmd, stop_on_errors=True, sudo=True)
    for host, host_output in output.items():
      for line in host_output.stdout:
        print(line)

def main():
  args = sys.argv[1:]
  app_dir = args[0]
  pkg_name = args[1]
  ver = args[2]
  itern = args[3]
  prefix = args[4]
  desc = args[5]
  host_rpm_build = ['inw-61']

  usage = ('build_dist_rpm.py <app dir> <pkg name> <version> <iteration> <prefix> <desc>\n'
           'Example: build_dist_rpm.py kafka_2.11-0.10.0.0 debezium-connect 0.6.0 1 /opt/debezium-connect/0.6.0 "debezium RPM package with new kafka libs"') 
  
  if not args or len(args) < 6:
    print usage
    sys.exit(1)

  fpm_cmd = 'fpm -s %s -t rpm -C %s --name %s --version %s --iteration %s --prefix %s --description %s .' % (app_dir, pkg_name, ver, itern, prefix, desc)   

ssh(host_rpm_build, fpm_cmd)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
