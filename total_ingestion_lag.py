#!/usr/bin/python

import sys
import re
from pssh.clients import ParallelSSHClient
import logging
from socket import timeout
import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run(host, pipeline):
    currentDT = datetime.datetime.now()
    lag = []
    x = "'{print $5}'"
    my_host_str = ''.join(host)
    cmd = "/apps/kafka/bin/kafka-consumer-groups.sh --bootstrap-server {}:9552 --describe --new-consumer --group {}ingestionconsumers | grep {} | awk {}".format(my_host_str, pipeline, pipeline, x)
    print 'Running cmd {}\n\n'.format(cmd)
    print 'Getting total lag from kafka host {}'.format(my_host_str)
    print 'Time: {}'.format(currentDT)
    failed_hosts = []
    logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler())
    client = ParallelSSHClient(host, timeout=5, user='VBhatia')
    output = client.run_command(cmd, stop_on_errors=False)
    for host, host_output in output.items():
        if host_output.exception is not None:
            failed_hosts.append(host)
        else:
            for line in host_output.stdout:
                lag.append(line) 
            #print '\r'
    lag_count = [int(i) for i in lag]
    total_lag = sum(lag_count)
    print bcolors.FAIL + 'Total lag: ' + str(total_lag) + bcolors.ENDC

    # Print ist of failed hosts
    if len(failed_hosts) > 0:
        print bcolors.FAIL + 'Unable to ssh to below host(s):' + bcolors.ENDC
        for x in failed_hosts:
            print bcolors.OKGREEN + x + bcolors.ENDC


def main():
    args = sys.argv[1:]
    usage = ('total_ingestion_lag.py <deployment> <pipeline>\n'
             'Example: total_ingestion_lag.py jpus journal03')
    if not args or len(args) < 1:
        print usage
        sys.exit(1)

    pipeline = args[1]

    jpus = ['fab-jpus01-kaf-h2']
    jpdr = ['fab-jpdr01-kaf-h2']
    emea = ['fab-emea01-kafzoo-h1']
    emdr = ['fab-emdr01-kafzoo-h1']
    apac = ['fab-apac01-kafzoo-h1'] 
    apdr = ['fab-apdr01-kafzoo-h1']
    jpuat = ['fab-jpuat01-kafzoo-h2']
    apuat = ['fab-apuat01-kafzoo-h1']
    emuat = ['fab-emuat01-kafzoo-h1']

    if args[0] == 'jpus':
        for host in jpus:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'jpdr':
        for host in jpdr:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'emea':
        for host in emea:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'emdr':
        for host in emdr:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'apac':
        for host in apac:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'apdr':
        for host in apdr:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'jpuat':
        for host in jpuat:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'apuat':
        for host in apuat:
            kafka_host = host.split()
            run(kafka_host, pipeline)
    elif args[0] == 'emuat':
        for host in emuat:
            kafka_host = host.split()
            run(kafka_host, pipeline)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
