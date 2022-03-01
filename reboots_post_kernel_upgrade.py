#!/usr/bin/env python

import commands
import sys
import re
import time
import os
import argparse

def check_session(filename):
    hosts_ready_to_reboot = []
    hosts_have_session = []
    with open(filename) as f:
        for line in f:
            host = line.strip('\n')
            if host.startswith('app'):
                cmd = 'knife ssh -m {} "ls /mnt/chrootusers/sessions/ | wc -l"'.format(host)
                (status, output) = commands.getstatusoutput(cmd)
                if status:    ## Error case, print the command's output to stderr and exit
                    sys.stderr.write(output)
                    sys.exit(status)
                my_list = output.split()
                host_name = my_list[0]
                session_num = int(my_list[1])
                if session_num == 0:
                    hosts_ready_to_reboot.append(host)
                else:
                    hosts_have_session.append(host)
            elif host.startswith('pchute') or host.startswith('egress'):
                cmd = 'knife ssh -m {} "sudo ipsec status | grep Security"'.format(host)
                (status, output) = commands.getstatusoutput(cmd)
                if status:    ## Error case, print the command's output to stderr and exit
                    sys.stderr.write(output)
                    sys.exit(status)
                my_list = output.split()
                host_name = my_list[0]
                connection_num_index = my_list[3]
                established_conn = int(connection_num_index.replace('(', ''))
                if established_conn == 0:
                    hosts_ready_to_reboot.append(host)
                else:
                    hosts_have_session.append(host)
    if len(hosts_ready_to_reboot) == 0:
        print 'All hosts checked have sessions. Nothing to reboot. Exiting...'
        sys.exit(1)
    else:
        create_files(hosts_ready_to_reboot, hosts_have_session, filename)

def create_files(hosts_ready_to_reboot, hosts_have_session, filename):
    with open('hosts_ready_to_reboot', 'w') as f:
        for host in hosts_ready_to_reboot:
            f.write(host + '\n')
    with open('hosts_have_sessions', 'w') as f:
        for host in hosts_have_session:
            f.write(host + '\n')
    # Remove hosts from the host file that have already been slated to be rebooted. Only keep the ones that still need a reboot (e.g. hosts_have_sessions)
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
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
    cmd = 'knife ssh -m "{}" "sudo systemctl reboot --force" -C {}'.format(host_str, host_num)
    os.system(cmd)
    run_chef(host_str, host_num)

def run_chef(host_str, host_num):
    time.sleep(300)
    cmd = 'knife ssh -m "{}" "sudo -i chef-client" -C {}'.format(host_str, host_num)
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description="App or Pchute reboots")
    parser.add_argument("filename", help="File containing hostnames[one on each line] to be rebooted")
    
    args = parser.parse_args()
    filename = args.filename
    
    check_session(filename)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
