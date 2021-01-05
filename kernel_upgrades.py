#!/usr/bin/env python

import commands
import sys
import re

def check_session(host_file):
    hosts_ready_to_reboot = []
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
                hosts_ready_to_reboot.append(host)
            else:
                hosts_have_session.append(host)
    create_files(hosts_ready_to_reboot, hosts_have_session)

def create_files(hosts_ready_to_reboot, hosts_have_session):
    with open('hosts_ready_to_reboot', 'a') as f:
        for host in hosts_ready_to_reboot:
            f.write(host + '\n')
    with open('hosts_have_sessions', 'a') as f:
        for host in hosts_have_session:
            f.write(host + '\n')


def main():
    args = sys.argv[1:]
    hosts_file = args[0]
    check_session(hosts_file)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
