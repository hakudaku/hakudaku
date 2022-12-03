#!/usr/bin/env python

import commands
import sys
import re
import time
import os
import argparse
from datetime import datetime, timedelta

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    HEADER = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_session(filename):
    now = datetime.now()
    sessions_greater_24_hrs = []
    hosts_OK_to_reboot = []
    hosts_NOT_OK_to_reboot = []
    with open(filename) as f:
        for line in f:
            host = line.strip('\n')
            if host.startswith('app') and 'lb' not in host:
                get_session_count_cmd = 'knife ssh -m {} "ls /mnt/chrootusers/sessions/ | wc -l"'.format(host)
                get_session_info_cmd = 'knife ssh -m {} "stat /mnt/chrootusers/sessions/*"'.format(host)
                (status, output) = commands.getstatusoutput(get_session_count_cmd)
                if status:    ## Error case, print the command's output to stderr and exit
                    sys.stderr.write(output)
                    sys.exit(status)
                session_list = output.split()
                session_num = int(session_list[1])
                if session_num > 0: # Only do stat if there are actually files/sessions present
                    (status, output) = commands.getstatusoutput(get_session_info_cmd)
                    if status:    ## Error case, print the command's output to stderr and exit
                        sys.stderr.write(output)
                        sys.exit(status)
                    dates = re.findall(r'Modify:\s+(\d\d\d\d-\d\d-\d\d\s+\d\d:\d\d:\d\d)\.+', output)
                    for d in dates:
                        my_datetime = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
                        if now - my_datetime > timedelta(1): # session older than 24 hours
                            sessions_greater_24_hrs.append(d)
                        if len(dates) == len(sessions_greater_24_hrs): # all sessions are older than 24 hours
                            all_sessions_old = True
                        elif len(dates) != len(sessions_greater_24_hrs):
                            all_sessions_old = False
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

            check_boot_part_space_cmd = 'knife ssh -m {} "df -h|egrep \'^File|/boot$\'"'.format(host)
            (boot_status, boot_output) = commands.getstatusoutput(check_boot_part_space_cmd)
            if not 'boot' in boot_output:
                print 'Boot partition not detected on host {}'.format(host) + ' ' + u'\u2705'
                boot = True
            else:
                boot_part_space = re.search(r'\S+\s+\d+M\s+\d+M\s+(\d+)M.+', boot_output)
                boot_part_space = int(boot_part_space.group(1))
                if boot_part_space < 100:
                    print '/boot partition < 100MB on {}. Kernel cleanup required'.format(host) + ' ' + u'\u274c'
                    boot = False
                else:
                    print '/boot partition > 100MB on {}. Kernel cleanup not required.'.format(host) + ' ' + u'\u2705'
                    boot = True

            check_if_fips_cmd = 'knife node show {}'.format(host)
            (fips_status, fips_output) = commands.getstatusoutput(check_if_fips_cmd)
            if 'fips' in fips_output:
                print bcolors.WARNING + '{} is a FIPS host. Checking HMAC...'.format(host) + bcolors.ENDC
                check_kernel_cmd = 'knife ssh -m {} "sudo cat /etc/default/grub.d/51-kernel.cfg"'.format(host)
                (kernel_status, kernel_output) = commands.getstatusoutput(check_kernel_cmd)
                kernel = re.search(r'.+Linux\s+(\S+)\"', kernel_output)
                check_hmac_pkg_cmd = 'knife ssh -m {} "sudo apt list --installed | grep linux-image-hmac-{}"'.format(host, kernel.group(1))
                check_hmac_pkg_cmd_exit_code = os.system(check_hmac_pkg_cmd)
                time.sleep(2)
                if check_hmac_pkg_cmd_exit_code == 0:
                    print 'Valid HMAC file found on host {}'.format(host) + ' ' + u'\u2705'
                else:
                    print 'hmac pkg for kernel {} not installed on {}, installing now...'.format(kernel.group(1), host) + ' ' + u'\u274c'
                    install_hmac_cmd = 'knife ssh -m {} "sudo apt -y install linux-image-hmac-{}"'.format(host, kernel.group(1))
                    os.system(install_hmac_cmd)
            else:
                print '{} is not a FIPS host, skipping HMAC check'.format(host) + ' ' + u'\u2705'


            if 'session_num' in locals() and session_num < 5 and boot != False:
                print '{} has 0 sessions...moving to reboot file'.format(host) + ' ' + u'\u2705'
                hosts_OK_to_reboot.append(host)
            elif 'session_num' in locals() and 'all_sessions_old' in locals() and session_num > 0 and boot != False and all_sessions_old == True:
                print '{} has sessions but all of them are older than 24 hours...moving to reboot file'.format(host) + ' ' + u'\u2705'
                hosts_OK_to_reboot.append(host)
            elif 'established_conn' in locals() and established_conn == 0 and boot != False:
                print '{} has 0 established_conn...moving to reboot file'.format(host) + ' ' + u'\u2705'
                hosts_OK_to_reboot.append(host)
            else:
                print '{} has current and active sessions/connections...not ready for reboot'.format(host) + ' ' + u'\u274c'
                hosts_NOT_OK_to_reboot.append(host)

    if len(hosts_OK_to_reboot) == 0:
        print bcolors.FAIL + 'One or more checks failed on ALL hosts! Nothing to reboot. Exiting...' + bcolors.ENDC
        sys.exit(1)
    else:
        create_files(hosts_OK_to_reboot, hosts_NOT_OK_to_reboot, filename)

def create_files(hosts_OK_to_reboot, hosts_NOT_OK_to_reboot, filename):
    with open('hosts_OK_to_reboot', 'w') as f:
        for host in hosts_OK_to_reboot:
            f.write(host + '\n')
    with open('hosts_NOT_OK_to_reboots', 'w') as f:
        for host in hosts_NOT_OK_to_reboot:
            f.write(host + '\n')
    # Remove hosts from the host file that have already been slated to be rebooted. Only keep the ones that still need a reboot (e.g. hosts_NOT_OK_to_reboots)
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        for line in lines:
            line_minus_new_line_char = line.strip()
            if line_minus_new_line_char in hosts_NOT_OK_to_reboot:
                f.write(line)

    reboot_em(hosts_OK_to_reboot)

def reboot_em(hosts_OK_to_reboot):
    host_num = len(hosts_OK_to_reboot)
    host_str = ' '.join(hosts_OK_to_reboot)
    time.sleep(2)
    print bcolors.FAIL + 'Hosts {} will reboot in 10 seconds'.format(host_str) + bcolors.ENDC
    time.sleep(10)
    cmd = 'knife ssh -m "{}" "echo T00m@nyp@55w0rd5 | sudo -S systemctl reboot --force" -C {}'.format(host_str, host_num)
    os.system(cmd)
    run_chef(host_str, host_num)

def run_chef(host_str, host_num):
    print 'Sleeping for 5 min while host(s) reboot'
    time.sleep(300)
    cmd = 'knife ssh -m "{}" "echo T00m@nyp@55w0rd5 | sudo -Si chef-client" -C {}'.format(host_str, host_num)
    os.system(cmd)


def main():
    parser = argparse.ArgumentParser(description="Server reboots")
    parser.add_argument("filename", help="File containing hostnames[one on each line] to be rebooted")

    args = parser.parse_args()
    filename = args.filename

    check_session(filename)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
