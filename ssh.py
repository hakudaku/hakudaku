#!/Users/vineetbhatia/ENV/bin/python -tt

import sys
import re
from pssh.clients import ParallelSSHClient
import logging
from socket import timeout
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ssh(hosts, cmd):
    failed_hosts = []
    logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler())
    client = ParallelSSHClient(hosts, timeout=5, user='vbhatia')
    output = client.run_command(cmd, stop_on_errors=False)
    for host, host_output in output.items():
        if  host_output.exception is not None:
            failed_hosts.append(host)
        else:
            for line in host_output.stdout:
                print line
            print '\r'

    # Print ist of failed hosts
    if len(failed_hosts) > 0:
        print bcolors.FAIL + 'Unable to ssh to below host(s):' + bcolors.ENDC
        for x in failed_hosts:
            print bcolors.BOLD + x + bcolors.ENDC

def main():
    parser = argparse.ArgumentParser(description="Run commands on multiple hosts in Parallel")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("cmd", help="Command to run on host")
    group.add_argument("-n", "--nodename", help="Hostname on which running command (Note: A file with hostnames\
                                          can be substituted - see --file option)")
    group.add_argument("-f", "--file", help="Specify file name with hostnames listed one on each line")

    args = parser.parse_args()
    cmd = 'hostname -f; {}'.format(args.cmd)
    host = ''
    if args.nodename:
        host = args.nodename
    hosts = []

    match_hyphen = re.search(r'^\S+\[\d+\-\d+\]', host)
    match_comma = re.search(r',', host)
    if match_hyphen:
        host_name = re.search(r'^(\S+)\[', host)
        host_colo = re.search(r'^\S+\[\S+](\S+)', host)
        num_match = re.search(r'(\d+)-(\d+)', host)
        int_1 = int(num_match.group(1))
        int_2 = int(num_match.group(2)) + 1
        for x in xrange(int_1, int_2):
            hosts.append(host_name.group(1) + str(x) + host_colo.group(1))
        ssh(hosts, cmd)
    elif match_comma:
        host_name = re.search(r'^(\S+)\[', host)
        host_colo = re.search(r'^\S+\[\S+](\S+)', host)
        num_match = re.findall(r'\W(\d+)', host)
        for num in num_match:
            hosts.append(host_name.group(1) + num + host_colo.group(1))
        ssh(hosts, cmd)

    elif args.file:
        host_file = args.file
        f = open(host_file, 'rU')
        for line in f:
            hosts.append(line.strip('\n'))
        ssh(hosts, cmd)

    else:
        hosts.append(host)
        ssh(hosts, cmd)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
