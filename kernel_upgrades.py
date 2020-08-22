#!/usr/bin/env python

import commands
import sys
import re

def check_session(host_file):
    hosts_to_upgrade = []
    hosts_have_session = []
    with open(host_file) as f:
        for line in f:
            host = line.strip('\n')
            cmd = 'knife ssh -m {} "ls /mnt/chrootusers/sessions/ | wc -l"'.format(host)
            (status, output) = commands.getstatusoutput(cmd)
            if status:    ## Error case, print the command's output to stderr and exit
                sys.stderr.write(output)
                sys.exit(status)
            my_list = output.split()
            host_name = my_list[0]
            session_num = my_list[1]
            if session_num == '0':
                hosts_to_upgrade.append(host)
            else:
                hosts_have_session.append(host)
    kernel_upgrade(hosts_to_upgrade, hosts_have_session)
        
def kernel_upgrade(hosts_to_upgrade, hosts_have_session):
    for host in hosts_to_upgrade:
        cmd = 'knife ssh -m {} "w"'.format(host)
        (status, output) = commands.getstatusoutput(cmd)
        if status:    ## Error case, print the command's output to stderr and exit
                sys.stderr.write(output)
                sys.exit(status)
        print output
    hosts_pending_upgrade(hosts_have_session)

def create_pending_hosts_file(hosts_have_session):
    with open('app_hosts_pending_kernel_update', 'a') as f:
        for host in hosts_have_session:
            f.write(host) 

def main():
    args = sys.argv[1:]
    hosts_file = args[0]
    check_session(hosts_file)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
