#!/usr/bin/python -tt

import sys
import re
import os
import datetime
import commands
import shutil

# Updating hostclass with a new pkg or new version of an existng pkg

def conf_change(file_path, hostclass, path_to_ops_config_queue):
  timestamp = datetime.datetime.today().strftime('%Y.%m.%d_%H.%M')
  cmd_commit = 'git commit -m "conf change" %s' % (file_path)
  cmd_push = 'git pull --rebase && ' + path_to_ops_config_queue
  cmd_tag = 'git tag %s-%s' % (hostclass, timestamp)
  cmd_push_tag = 'git push --tags'
  cmd_git_diff = 'git diff'
  cmd_git_status = 'git status'
  cmd_revert = 'git checkout %s' % file_path

  (status, output) = commands.getstatusoutput(cmd_git_status)
  (diff_status, diff_output) = commands.getstatusoutput(cmd_git_diff)
  
  print output
  print '\n'
  print diff_output

  commit_ans = raw_input('Ready to commit? y/n: ')
  if commit_ans == 'n':
    revert_ans = raw_input('Revert the changes? y/n: ')
    if revert_ans == 'y':
      (status, output) = commands.getstatusoutput(cmd_revert)
      if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(1)
      print output  ## Otherwise do something with the command's output    

  if commit_ans == 'y':
    create_new_hostclass_git_tag(cmd_commit, cmd_push, cmd_tag, cmd_push_tag)


def update_hostclass_new_pkg(file_path, pkg_full, hostclass, path_to_ops_config_queue):
  timestamp = datetime.datetime.today().strftime('%Y.%m.%d_%H.%M')
  cmd_commit = 'git commit -m "add %s" %s' % (pkg_full, file_path)
  cmd_push = 'git pull --rebase && ' + path_to_ops_config_queue
  cmd_tag = 'git tag %s-%s' % (hostclass, timestamp)
  cmd_push_tag = 'git push --tags'
  cmd_git_diff = 'git diff'
  cmd_git_status = 'git status'
  cmd_revert = 'git checkout %s' % file_path
      
  f = open(file_path, 'r')
  f_new = open('hostclass_tmp', 'w')
  for line in f:
    f_new.write(line)
    if 'production' in line:
      f_new.write('  - ' + pkg_full + '\n')
  f.close()
  f_new.close()
  shutil.move('hostclass_tmp', file_path)

  (status, output) = commands.getstatusoutput(cmd_git_status)
  (diff_status, diff_output) = commands.getstatusoutput(cmd_git_diff)
  
  print output
  print '\n'
  print diff_output

  commit_ans = raw_input('Ready to commit? y/n: ')
  if commit_ans == 'n':
    revert_ans = raw_input('Revert the changes? y/n: ')
    if revert_ans == 'y':
      (status, output) = commands.getstatusoutput(cmd_revert)
      if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(1)
      print output  ## Otherwise do something with the command's output    

  if commit_ans == 'y':
    create_new_hostclass_git_tag(cmd_commit, cmd_push, cmd_tag, cmd_push_tag)    


def update_hostclass_new_version(file_path, pkg_base, pkg_full, hostclass, path_to_ops_config_queue):
  timestamp = datetime.datetime.today().strftime('%Y.%m.%d_%H.%M')
  cmd_commit = 'git commit -m "bump %s" %s' % (pkg_base.group(), file_path)
  cmd_push = 'git pull --rebase &&' + path_to_ops_config_queue
  cmd_tag = 'git tag %s-%s' % (hostclass, timestamp)
  cmd_push_tag = 'git push --tags'
  cmd_git_diff = 'git diff'
  cmd_git_status = 'git status'
  cmd_revert = 'git checkout %s' % file_path
  
  f = open(file_path, 'r')
  for line in f:
    match = re.search(pkg_base.group() + '\S+', line)
    if match:
      f = open(file_path, 'r')
      data = f.read()
      data = data.replace(match.group(), pkg_full)
      f = open(file_path, 'w')
      f.write(data)
      f.close()
  
  (status, output) = commands.getstatusoutput(cmd_git_status)
  (diff_status, diff_output) = commands.getstatusoutput(cmd_git_diff)
  
  print output
  print '\n'
  print diff_output

  commit_ans = raw_input('Ready to commit? y/n: ')
  if commit_ans == 'n':
    revert_ans = raw_input('Revert the changes? y/n: ')
    if revert_ans == 'y':
      (status, output) = commands.getstatusoutput(cmd_revert)
      if status:    ## Error case, print the command's output to stderr and exit
        sys.stderr.write(output)
        sys.exit(1)
      print output  ## Otherwise do something with the command's output    
  
  if commit_ans == 'y':
    create_new_hostclass_git_tag(cmd_commit, cmd_push, cmd_tag, cmd_push_tag)
  
def create_new_hostclass_git_tag(cmd_commit, cmd_push, cmd_tag, cmd_push_tag):
  all_cmds = [cmd_commit, cmd_push, cmd_tag, cmd_push_tag]
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

  if args[1] == '--conf':
    hostclass = args[0]
    path_to_ops_config_queue = os.path.expanduser('~') + '/ops-config/bin/ops-config-queue'
    path_to_hostclass_yml = os.path.expanduser('~') + '/ops-config/hostclasses/%s.yml' % hostclass

    conf_change(path_to_hostclass_yml, hostclass, path_to_ops_config_queue )

  elif args[2] == '--new':
    pkg_full = args[1]
    hostclass = args[0]
    path_to_ops_config_queue = os.path.expanduser('~') + '/ops-config/bin/ops-config-queue'
    path_to_hostclass_yml = os.path.expanduser('~') + '/ops-config/hostclasses/%s.yml' % hostclass

    update_hostclass_new_pkg(path_to_hostclass_yml, pkg_full, hostclass, path_to_ops_config_queue )
  
  elif args[2] == '--update':
    pkg_full = args[1]
    pkg_base = re.search('\w+', pkg_full)
    hostclass = args[0]
    path_to_ops_config_queue = os.path.expanduser('~') + '/ops-config/bin/ops-config-queue'
    path_to_hostclass_yml = os.path.expanduser('~') + '/ops-config/hostclasses/%s.yml' % hostclass
  
    update_hostclass_new_version(path_to_hostclass_yml, pkg_base, pkg_full, hostclass, path_to_ops_config_queue)
  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
