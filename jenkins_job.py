#!/Users/vineetbhatia/ENV/bin/python -tt
import json 
import requests
import urllib2
import time
import sys
import re
#from __future__ import print_function
from pssh import ParallelSSHClient
import paramiko, base64
import logging
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ssh(host, cmds):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(host)
  for cmd in cmds:
    print bcolors.FAIL + 'Running %s...' % cmd + bcolors.ENDC
    output = client.run_command(cmd, stop_on_errors=True, sudo=True)
    for host, host_output in output.items():
      for line in host_output.stdout:
        print(line)
      
def build_rpm(build_url, user, token, poll_url, payload, host, build_num):
  r = requests.post(build_url, auth=(user, token), data=payload)
  print(r.text)
  
  time.sleep(10) 
  
  while True:
    r = requests.get(poll_url, auth=(user, token), data=payload)
    if 'SUCCESS' in r.text:
      rpm_match = re.search(r'.+(rfi-infradb-rails4.+\.rpm)', r.text)
      rpm_file = rpm_match.group(1) 
      print 'RPM', rpm_file, 'created successfully!'
      break
  puppet_down = 'svc -d /service/puppet4'
  yum_remove = 'yum remove rfi-infradb-rails4 -y'
  yum_install = 'yum install https://jenkins.rfiserve.net/job/puppet4-custom-rpm/%s/artifact/build/rpmbuild-rfi-infradb/RPMS/noarch/%s -y' % (build_num, rpm_file)
  test_script = '/opt/infradb4/puppet/code/environments/production/modules/rfi/files/standalone.sh'
  cmds = [puppet_down, yum_remove, yum_install, test_script]
  ssh(host, cmds)
    

def main():
  args = sys.argv[1:]
  usage = ('jenkins_job.py <id> <patch> <build> <host>\n'
           'Example: jenkins_job.py 126418 0 103 lsv-1746')
  if not args or len(args) < 4:
    print usage
    sys.exit(1)
  pr_id = args[0]  
  pr_patch = args[1]
  build_num = args[2]
  host = [args[3]]
  user = 'vbhatia'
  token = '6252cf9d6b13db98f254619f00173ad4'
  build_url = 'https://jenkins.rfiserve.net/job/puppet4-custom-rpm/buildWithParameters'
  poll_url = 'https://jenkins.rfiserve.net/job/puppet4-custom-rpm/%s/logText/progressiveText?start=0' % build_num
  payload = {'GERRIT_PR_ID': pr_id, 'GERRIT_PR_PATCHSET': pr_patch}
  build_rpm(build_url, user, token, poll_url, payload, host, build_num)
  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()

