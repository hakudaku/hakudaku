#!/usr/bin/python

import sys
import re
from pssh.clients import ParallelSSHClient
import logging
from socket import timeout
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run(host, cmd):
    my_host_str = ''.join(host)
    print 'Running command {} on host {}'.format(cmd, my_host_str) 
    failed_hosts = []
    logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler())
    client = ParallelSSHClient(host, timeout=5, user='VBhatia')
    output = client.run_command(cmd, stop_on_errors=False)
    for host, host_output in output.items():
        if host_output.exception is not None:
            failed_hosts.append(host)
        else:
            for line in host_output.stdout:
                print line
            print '\r'
    print 'Host {} restart complete!!!\n'.format(host)

    # Print ist of failed hosts
    if len(failed_hosts) > 0:
        print bcolors.FAIL + 'Unable to ssh to below host(s):' + bcolors.ENDC
        for x in failed_hosts:
            print bcolors.BOLD + x + bcolors.ENDC


def main():
    args = sys.argv[1:]
    usage = ('haz_restarts.py [cluster]\n'
             'Example: haz_restarts.py jpus')
    if not args or len(args) < 1:
        print usage
        sys.exit(1)

    cmd = 'sudo systemctl stop hazelcast;sleep 10;sudo systemctl start hazelcast'

    jpus = ['fab-jpus01-haz-h4', 'fab-jpus01-haz-h5', 'fab-jpus01-haz-h6']
    jpdr = ['fab-jpdr01-haz-h4', 'fab-jpdr01-haz-h5', 'fab-jpdr01-haz-h6']
    emea = ['fab-emea01-haz-h1', 'fab-emea01-haz-h2', 'fab-emea01-haz-h3']
    emdr = ['fab-emdr01-haz-h1', 'fab-emdr01-haz-h2', 'fab-emdr01-haz-h3']
    apac = ['fab-apac01-haz-h1', 'fab-apac01-haz-h2', 'fab-apac01-haz-h3'] 
    apdr = ['fab-apdr01-haz-h1', 'fab-apdr01-haz-h2', 'fab-apdr01-haz-h3']
    jpuat = ['fab-jpuat01-haz-h1', 'fab-jpuat01-haz-h2', 'fab-jpuat01-haz-h4']
    apuat = ['fab-apuat01-haz-h3']
    emuat = ['fab-emuat01-haz-h1', 'fab-emuat01-haz-h2', 'fab-emuat01-haz-h3']

    if args[0] == 'jpus':
        for host in jpus:
            haz = host.split()
            run(haz, cmd)
            time.sleep(300)
    elif args[0] == 'jpdr':
        for host in jpdr:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'emea':
        for host in emea:
            haz = host.split()
            run(haz, cmd)
            time.sleep(300)
    elif args[0] == 'emdr':
        for host in emdr:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'apac':
        for host in apac:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'apdr':
        for host in apdr:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'jpuat':
        for host in jpuat:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'apuat':
        for host in apuat:
            haz = host.split()
            run(haz, cmd)
    elif args[0] == 'emuat':
        for host in emuat:
            haz = host.split()
            run(haz, cmd)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
