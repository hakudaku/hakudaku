#!/usr/bin/python -tt

import sys
import re
import os
import datetime
import commands
import shutil

# Updating hostclass with a new pkg or new version of an existng pkg

class hostclass_tag(object):
  
  def __init__(self, path_to_hostclass_yml, pkg_base, pkg_full, hostclass, path_to_ops_config_queue, cmd_commit, cmd_push, cmd_tag, cmd_push_tag, cmd_git_diff, cmd_git_status, cmd_revert):
    self.path_to_hostclass_yml = path_to_hostclass_yml
    self.pkg_base = pkg_base
    self.pkg_full = pkg_full
    self.hostclass = hostclass
    self.path_to_ops_config_queue = path_to_ops_config_queue
    self.cmd_commit = cmd_commit
    self.cmd_push = cmd_push
    self.cmd_tag = cmd_tag
    self.cmd_push_tag = cmd_push_tag
    self.cmd_git_diff = cmd_git_diff
    self.cmd_git_status = cmd_git_status
    self.cmd_revert = cmd_revert


  def conf_change(self):
    (status, output) = commands.getstatusoutput(self.cmd_git_status)
    (diff_status, diff_output) = commands.getstatusoutput(self.cmd_git_diff)
  
    print output
    print '\n'
    print diff_output

    commit_ans = raw_input('Ready to commit? y/n: ')
    if commit_ans == 'n':
      revert_ans = raw_input('Revert the changes? y/n: ')
      if revert_ans == 'y':
        (status, output) = commands.getstatusoutput(self.cmd_revert)
        if status:    ## Error case, print the command's output to stderr and exit
          sys.stderr.write(output)
          sys.exit(1)
        print output  ## Otherwise do something with the command's output

    if commit_ans == 'y':
      self.create_new_hostclass_git_tag()


  def update_hostclass_new_pkg(self):
      
    f = open(self.path_to_hostclass_yml, 'r')
    f_new = open('hostclass_tmp', 'w')
    for line in f:
      f_new.write(line)
      if 'production' in line:
        f_new.write('  - ' + self.pkg_full + '\n')
    f.close()
    f_new.close()
    shutil.move('hostclass_tmp', self.path_to_hostclass_yml)

    (status, output) = commands.getstatusoutput(self.cmd_git_status)
    (diff_status, diff_output) = commands.getstatusoutput(self.cmd_git_diff)
  
    print output
    print '\n'
    print diff_output

    commit_ans = raw_input('Ready to commit? y/n: ')
    if commit_ans == 'n':
      revert_ans = raw_input('Revert the changes? y/n: ')
      if revert_ans == 'y':
        (status, output) = commands.getstatusoutput(self.cmd_revert)
        if status:    ## Error case, print the command's output to stderr and exit
          sys.stderr.write(output)
          sys.exit(1)
        print output  ## Otherwise do something with the command's output

    if commit_ans == 'y':
      self.create_new_hostclass_git_tag()


  def update_hostclass_new_version(self):
  
    f = open(self.path_to_hostclass_yml, 'r')
    for line in f:
      match = re.search(self.pkg_base.group() + '\S+', line)
      if match:
        f = open(self.path_to_hostclass_yml, 'r')
        data = f.read()
        data = data.replace(match.group(), self.pkg_full)
        f = open(self.path_to_hostclass_yml, 'w')
        f.write(data)
        f.close()
  
    (status, output) = commands.getstatusoutput(self.cmd_git_status)
    (diff_status, diff_output) = commands.getstatusoutput(self.cmd_git_diff)
  
    print output
    print '\n'
    print diff_output

    commit_ans = raw_input('Ready to commit? y/n: ')
    if commit_ans == 'n':
      revert_ans = raw_input('Revert the changes? y/n: ')
      if revert_ans == 'y':
        (status, output) = commands.getstatusoutput(self.cmd_revert)
        if status:    ## Error case, print the command's output to stderr and exit
          sys.stderr.write(output)
          sys.exit(1)
        print output  ## Otherwise do something with the command's output
  
    if commit_ans == 'y':
      self.create_new_hostclass_git_tag()
  
  def create_new_hostclass_git_tag(self):
    all_cmds = [self.cmd_commit, self.cmd_push, self.cmd_tag, self.cmd_push_tag]
    for cmd in all_cmds:
      (status, output) = commands.getstatusoutput(cmd)
      if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(1)
      print output  ## Otherwise do something with the command's output
   

def main():
  args = sys.argv[1:]
  if not args:
    print ('Usage: <script_name> <hostclass> [pkg_name] [--conf] [--new] [--update]')
    sys.exit(1)

  hostclass = args[0]
  pkg_full = args[1]
  pkg_base = re.search('\w+', pkg_full)
  path_to_ops_config_queue = os.path.expanduser('~') + '/ops-config/bin/ops-config-queue'
  path_to_hostclass_yml = os.path.expanduser('~') + '/ops-config/hostclasses/%s.yml' % hostclass

  timestamp = datetime.datetime.today().strftime('%Y.%m.%d_%H.%M')
  cmd_commit = 'git commit -m "bump %s" %s' % (pkg_base.group(), path_to_hostclass_yml)
  cmd_push = 'git pull --rebase &&' + path_to_ops_config_queue
  cmd_tag = 'git tag %s-%s' % (hostclass, timestamp)
  cmd_push_tag = 'git push --tags'
  cmd_git_diff = 'git diff'
  cmd_git_status = 'git status'
  cmd_revert = 'git checkout %s' % path_to_hostclass_yml

  my_instance = hostclass_tag(path_to_hostclass_yml, pkg_base, pkg_full, hostclass, path_to_ops_config_queue, cmd_commit, cmd_push, cmd_tag, cmd_push_tag, cmd_git_diff, cmd_git_status, cmd_revert)

  if args[1] == '--conf':
    my_instance.conf_change()

  elif args[2] == '--new':
    my_instance.update_hostclass_new_pkg()

  elif args[2] == '--update':
    my_instance.update_hostclass_new_version()

  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
