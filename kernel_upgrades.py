#!/usr/bin/env python

import commands
import sys
import re
import time
import os

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
    if len(hosts_ready_to_reboot) == 0:
        print 'All hosts checked have sessions. Nothing to reboot. Exiting...'
        sys.exit(1)
    else:
        create_files(hosts_ready_to_reboot, hosts_have_session, host_file)

def create_files(hosts_ready_to_reboot, hosts_have_session, host_file):
    with open('hosts_ready_to_reboot', 'w') as f:
        for host in hosts_ready_to_reboot:
            f.write(host + '\n')
    with open('hosts_have_sessions', 'w') as f:
        for host in hosts_have_session:
            f.write(host + '\n')
    # Remove hosts from the host file that have already been slated to be rebooted. Only keep the ones that still need a reboot (e.g. hosts_have_sessions)
    with open(host_file, 'r') as f:
        lines = f.readlines()
    with open(host_file, 'w') as f:
        for line in lines:
            line_minus_new_line_char = line.strip()
            if line_minus_new_line_char in hosts_have_session:
                f.write(line)

    reboot_em(hosts_ready_to_reboot)

def reboot_em(hosts_ready_to_reboot):
    host_num = len(hosts_ready_to_reboot)
    host_str = ' '.join(hosts_ready_to_reboot)
    print 'Hosts {} will reboot in 10 seconds'.format(host_str)
    time.sleep(10)
    cmd = 'knife ssh -m "{}" "sudo init 6" -C {}'.format(host_str, host_num)
    os.system(cmd)


def main():
    args = sys.argv[1:]
    hosts_file = args[0]
    check_session(hosts_file)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
