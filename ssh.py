#!/Users/vbhatia/ENV/bin/python -tt

import sys
import re
from pssh import ParallelSSHClient
import paramiko
import base64
import logging
from socket import gethostbyname, gaierror, timeout
import argparse


def ssh(hosts, cmd):
    failed_hosts = []
    logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler())
    client = ParallelSSHClient(hosts, timeout=5)
    output = client.run_command(cmd, stop_on_errors=False)
    for host in output:
        for line in output[host]['stdout']:
            print line
        print '\r'
        if output[host]['exception'] is not None:
            print '***********Check Host {}. It is either down, invalid, or\
                   authentication failed*************\n'.format(host)
        if output[host]['exit_code'] != 0:
            failed_hosts.append(host)
    if len(failed_hosts) > 0:
        print '***Hosts failed***'
    for host in failed_hosts:
        print host


def ssh2(host, cmd):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, timeout=5)
        stdin, stdout, stderr = client.exec_command(cmd)
        for line in stdout:
            print line.strip('\n')
        for line in stderr:
            print line.strip('\n')
        print '\r'
        client.close()
    except (gaierror, timeout):
        print '***********Check Host {}. It is either down, invalid, or\
               authentication failed*************\n'.format(host)


def main():

    parser = argparse.ArgumentParser(description="Run commands on multiple hosts in Parallel")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("cmd", help="Command to run on host")
    group.add_argument("-n", "--nodename", help="Hostname on which running command (Note: A file with hostnames\
                                          can be substituted - see --file option)")
    group.add_argument("-f", "--file", help="Specify file name with hostnames listed one on each line")
    parser.add_argument("-p", "--parallel", help="Run command on multiple hosts in parallel",
                        action="store_true")
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
        if args.parallel:
            ssh(hosts, cmd)
        else:
            for host in hosts:
                ssh2(host, cmd)
    elif match_comma:
        host_name = re.search(r'^(\S+)\[', host)
        host_colo = re.search(r'^\S+\[\S+](\S+)', host)
        num_match = re.findall(r'\W(\d+)', host)
        for num in num_match:
            hosts.append(host_name.group(1) + num + host_colo.group(1))
        if args.parallel:
            ssh(hosts, cmd)
        else:
            for host in hosts:
                ssh2(host, cmd)
    elif args.file:
        host_file = args.file
        f = open(host_file, 'rU')
        for line in f:
            hosts.append(line.strip('\n'))
        if args.parallel:
            ssh(hosts, cmd)
        else:
            for host in hosts:
                ssh2(host, cmd)
    else:
        ssh2(host, cmd)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
