#!/usr/bin/python

import sys
import requests
from pssh.clients import ParallelSSHClient
import logging
from socket import timeout

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_drain_rate(host, pipeline):
    cmd = 'ls -trh /logs/storm/workers.artifacts | grep {} | tail -1'.format(pipeline) 
    logging.getLogger('pssh.ssh_client').addHandler(logging.NullHandler())
    client = ParallelSSHClient(host, timeout=5, user='VBhatia')
    output = client.run_command(cmd, stop_on_errors=False)
    for host, host_output in output.items():
        for line in host_output.stdout:
            journal_id = line
    my_host_str = ''.join(host)
    url = 'http://{}:3050/api/v1/topology/{}'.format(my_host_str, journal_id)
    r = requests.request('GET', url)
    dict_out =  r.json()
    my_dict = dict_out["topologyStats"][0]
    acked = my_dict['acked']
    failed = my_dict['failed']
    print 'Acked: {}'.format(acked)
    print 'Failed: {}'.format(failed)

def main():
    args = sys.argv[1:]
    usage = ('get_ingestion_drain_rate.py <deployment> <pipeline>\n'
             'Example template: get_ingestion_drain_rate.py [jpus] [jpdr] [journal01] [journal02] [journal03] [journal04] [vantage01] [lfs] [supervision] [reprocess]\n'
             'Example: get_ingestion_drain_rate.py jpdr journal01')
    if not args or len(args) < 2:
        print usage
        sys.exit(1)

    jpus_pri_stm = ['10.171.180.5']
    jpus_j01_stm = ['10.171.180.42'] 
    jpus_j02_stm = ['10.171.180.47']
    jpus_j03_stm = ['10.171.180.7']
    jpus_j04_stm = ['10.171.180.40']
    jpus_sup_stm = ['10.171.180.85']

    jpdr_pri_stm = ['10.183.111.5']
    jpdr_j01_stm = ['10.183.111.46']
    jpdr_j02_stm = ['10.183.111.6']
    jpdr_j03_stm = ['10.183.111.7']
    jpdr_j04_stm = ['10.183.111.39']
    jpdr_van01_stm = ['10.183.111.41']
    jpdr_lfs_stm = ['10.183.111.5']
    jpdr_sup_stm = ['10.183.111.85']
    jpdr_reproc_stm = ['10.183.111.40']

    if args[0] == 'jpdr' and args[1] == 'journal01':
        get_drain_rate(jpdr_j01_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'journal02':
        get_drain_rate(jpdr_j02_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'journal03':
        get_drain_rate(jpdr_j03_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'journal04':
        get_drain_rate(jpdr_j04_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'vantage01':
        get_drain_rate(jpdr_van01_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'lfs':
        get_drain_rate(jpdr_lfs_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'supervision':
        get_drain_rate(jpdr_sup_stm, args[1])

    elif args[0] == 'jpdr' and args[1] == 'reprocess':
        get_drain_rate(jpdr_reproc_stm, args[1])

    elif args[0] == 'jpus' and args[1] == 'journal01':
                get_drain_rate(jpus_j01_stm, args[1])

    elif args[0] == 'jpus' and args[1] == 'journal02':
                        get_drain_rate(jpus_j02_stm, args[1])

    elif args[0] == 'jpus' and args[1] == 'journal03':
                        get_drain_rate(jpus_j03_stm, args[1])

    elif args[0] == 'jpus' and args[1] == 'journal04':
                        get_drain_rate(jpus_j04_stm, args[1])

    elif args[0] == 'jpus' and args[1] == 'supervision':
                        get_drain_rate(jpus_sup_stm, args[1])


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
