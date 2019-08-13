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
    my_dict_ten_min = dict_out["topologyStats"][0]
    my_dict_three_hour = dict_out["topologyStats"][1]
    my_dict_one_day = dict_out["topologyStats"][2]
    my_dict_all_time = dict_out["topologyStats"][3]

    ten_min_acked = my_dict_ten_min['acked']
    three_hour_acked = my_dict_three_hour['acked']
    one_day_acked = my_dict_one_day['acked']
    all_time_acked = my_dict_all_time['acked']

    ten_min_failed = my_dict_ten_min['failed']
    three_hour_failed = my_dict_three_hour['failed']
    one_day_failed = my_dict_one_day['failed']
    all_time_failed = my_dict_all_time['failed']

    ten_min_drain_rate = ten_min_acked/600

    print '10m Acked: {}'.format(ten_min_acked)
    print '10m Failed: {}\n'.format(ten_min_failed)
    print '3h Acked: {}'.format(three_hour_acked)
    print '3h Failed: {}\n'.format(three_hour_failed)
    print '1d Acked: {}'.format(one_day_acked)
    print '1d Failed: {}\n'.format(one_day_failed)
    print 'All time Acked: {}'.format(all_time_acked)
    print 'All time Failed: {}\n'.format(all_time_failed)
    print '10m drain rate: {} per second'.format(ten_min_drain_rate)


def main():
    args = sys.argv[1:]
    usage = ('get_ingestion_drain_rate.py <deployment> <pipeline>\n'
             'Example template: get_ingestion_drain_rate.py [jpus] [jpdr] [apac] [emea] [jpuat] [journal01] [journal02] [journal03] [journal04] [vantage01] [lfs] [supervision] [reprocess]\n'
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
    
    apac_van01_stm = ['10.171.178.166']
    apac_sup_stm = ['10.171.178.207']
    apac_j01_stm = ['10.171.178.234']

    emea_sup_stm = ['10.165.224.77']
    jpuat_sup_stm = ['10.170.57.249']


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
    
    elif args[0] == 'apac' and args[1] == 'vantage01':
        get_drain_rate(apac_van01_stm, args[1])

    elif args[0] == 'apac' and args[1] == 'supervision':
        get_drain_rate(apac_sup_stm, args[1])

    elif args[0] == 'apac' and args[1] == 'journal01':
        get_drain_rate(apac_j01_stm, args[1])

    elif args[0] == 'emea' and args[1] == 'supervision':
        get_drain_rate(emea_sup_stm, args[1])

    elif args[0] == 'jpuat' and args[1] == 'supervision':
        get_drain_rate(jpuat_sup_stm, args[1])


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
