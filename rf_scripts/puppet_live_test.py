#!/Users/vineetbhatia/ENV/bin/python -tt
import sys
from pssh import ParallelSSHClient
import logging
import re

def run(host, cmd):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(host)
  output = client.run_command(cmd, stop_on_errors=True, sudo=True)
  for host in output:
    print host + ':'
    for line in output[host]['stdout']:
      print line

def revert(host, cmd):
  logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler()) #Adding NullHandler to the logger
  client = ParallelSSHClient(host)
  output = client.run_command(cmd, stop_on_errors=True, sudo=True)
  for host in output:
    print host + ':'
    for line in output[host]['stdout']:
      print line

def main():
  args = sys.argv[1:]
  usage = ('puppet_live_test.py [host] [repo] [cherry-pick-url-file]\n'
           'Example: puppet_live_test.py inw-186.rfiserve.net puppet cherry_pick_url.txt\n'
           'Example for reverting: puppet_live_test.py [host] [revert]')

  if not args:
    print usage
    sys.exit(1)

  if 'revert' in args:
    host = []
    host.append(args[0])
    cmd = 'unset;svc -u /service/puppet'
    revert(host, cmd)
  else:
    host = [] 
    host.append(args[0])
    repo = args[1]
    pup_down_cmd = 'svc -d /service/puppet'
    pup_force_cmd = 'puppetnow force'
    infra_reset_cmd = 'export INFRADB_SKIP_RESET=true'
    pup_reset_cmd = 'export PUPPET_SKIP_RESET=true'
    su_cmd = 'sudo su -'
    chdir_pup = 'cd /opt/puppet-data/puppet'
    chdir_infra = 'cd /opt/puppet-data/infradb'
    cherry_pick_url_file = args[2]


    if repo == 'puppet':
      f = open(cherry_pick_url_file, 'rU')
      for line in f:
        git_fetch_cmd = line.strip()
        match = re.search(r'^git\s+\S+\s+(\S+).', git_fetch_cmd)
        orig_str = match.group(1)
        replace_string = 'http://git.rfiserve.net:29419/operations/puppet.git'
        git_fetch_cmd = git_fetch_cmd.replace(orig_str, replace_string)
        cmd = '%s;%s;%s;%s;%s' % (pup_down_cmd, chdir_pup, git_fetch_cmd, pup_reset_cmd, pup_force_cmd)
        run(host, cmd)
    elif repo == 'infradb':
      f = open(cherry_pick_url_file, 'rU')
      for line in f:
        git_fetch_cmd = line
        match = re.search(r'^git\s+\S+\s+(\S+).', git_fetch_cmd)
        orig_str = match.group(1)
        replace_string = 'http://git.rfiserve.net:29419/operations/infradb.git'
        git_fetch_cmd = git_fetch_cmd.replace(orig_str, replace_string)
        cmd = '%s;%s;%s;%s;%s' % (pup_down_cmd, chdir_pup, git_fetch_cmd, infra_reset_cmd, pup_force_cmd)
        run(host, cmd)
    else:
      print usage

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
